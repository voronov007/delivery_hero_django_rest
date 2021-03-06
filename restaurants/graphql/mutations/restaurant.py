import graphene

from ..types import RestaurantInput, RestaurantType, UpdateRestaurantInput
from ...models import Restaurant


class CreateRestaurant(graphene.Mutation):
    class Arguments:
        restaurant_data = RestaurantInput(required=True)

    ok = graphene.Boolean()
    message = graphene.String()
    restaurant = graphene.Field(lambda: RestaurantType)

    @staticmethod
    def mutate(root, info, restaurant_data: RestaurantInput):
        if Restaurant.objects.filter(name=restaurant_data.name).exists():
            message = "Restaurant with such name already exists"
            return CreateRestaurant(ok=False, message=message)

        data = {
            "name": restaurant_data.name,
            "opens_at": restaurant_data.opens_at,
            "closes_at": restaurant_data.closes_at
        }

        try:
            r = Restaurant.objects.create(**data)
        except Exception as e:
            ok = False
            message = f"Exception during object creation: {e}"
            CreateRestaurant(ok=ok, message=message)
        else:
            ok = True
            return CreateRestaurant(ok=ok, message='', restaurant=r)


class UpdateRestaurant(graphene.Mutation):
    class Arguments:
        restaurant_update_data = UpdateRestaurantInput(required=True)

    ok = graphene.Boolean()
    message = graphene.String()
    restaurant = graphene.Field(lambda: RestaurantType)

    @staticmethod
    def mutate(root, info, restaurant_update_data: RestaurantInput):
        r_id = restaurant_update_data.id
        try:
            r = Restaurant.objects.get(pk=r_id)
        except:
            message = f"Restaurant with id={r_id} was not found"
            return UpdateRestaurant(ok=False, message=message)

        if restaurant_update_data.name:
            r.name = restaurant_update_data.name
        if restaurant_update_data.closes_at:
            r.closes_at = restaurant_update_data.closes_at
        if restaurant_update_data.opens_at:
            r.opens_at = restaurant_update_data.opens_at
        r.save()

        return UpdateRestaurant(ok=True, message="", restaurant=r)
