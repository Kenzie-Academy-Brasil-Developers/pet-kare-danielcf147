from rest_framework.views import APIView, Response, Request, status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Pet
from groups.models import Group
from traits.models import Trait
from .serializers import PetSerializer


class Petview(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        query_params = request.query_params.get("trait", None)

        if query_params:
            try:
                hairy_trait = Trait.objects.get(name=query_params)
            except Trait.DoesNotExist:
                return Response(
                    {"error": "Trait does not exist"}, status.HTTP_400_BAD_REQUEST
                )

            try:
                pets = Pet.objects.filter(traits=hairy_trait)
            except Pet.DoesNotExist:
                return Response(
                    {"error": "Pets with that trait do not exist"},
                    status.HTTP_400_BAD_REQUEST,
                )

            result_page = self.paginate_queryset(pets, request)

            serializer = PetSerializer(result_page, many=True)

            return self.get_paginated_response(serializer.data)

        pets = Pet.objects.all()

        result_page = self.paginate_queryset(pets, request)

        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_list = serializer.validated_data.pop("group")
        traits_list = serializer.validated_data.pop("traits")

        group_obj = Group.objects.filter(
            scientific_name__iexact=group_list["scientific_name"]
        ).first()

        if not group_obj:
            group_obj = Group.objects.create(**group_list)

        pet_obj = Pet.objects.create(**serializer.validated_data, group=group_obj)

        for traits_dict in traits_list:
            traits_obj = Trait.objects.filter(name__iexact=traits_dict["name"]).first()

            if not traits_obj:
                traits_obj = Trait.objects.create(**traits_dict)

            pet_obj.traits.add(traits_obj)

        serializer = PetSerializer(pet_obj)

        return Response(serializer.data, status.HTTP_201_CREATED)


class PetDetailView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:

        pets = Pet.objects.filter(pk=pet_id).first()
        serializer = PetSerializer(pets)

        return Response(serializer.data)

    def patch(self, request: Request, pet_id: int) -> Response:

        pet = get_object_or_404(Pet, pk=pet_id)

        serializer = PetSerializer(pet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        traits_data: list = serializer.validated_data.pop("traits", [])
        group_data: dict = serializer.validated_data.pop("group", None)

        pet.traits.clear()
        for trait_data in traits_data:
            trait, _ = Trait.objects.update_or_create(
                name__iexact=trait_data["name"], defaults=trait_data
            )
            pet.traits.add(trait)

        if group_data:
            group, _ = Group.objects.update_or_create(
                scientific_name__iexact=group_data["scientific_name"],
                defaults=group_data,
            )
            pet.group = group
            pet.save()

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(pet)

        return Response(serializer.data)

    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, pk=pet_id)

        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
