from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Itinerary, Attraction, ParkArea, Customer


class ItinerarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name='itinerary',
            lookup_field='id'
        )
        fields = ('id', 'url', 'starttime', 'attraction', 'customer_id')
        depth = 1


class Itineraries(ViewSet):

    def create(self, request):
        
        attraction = Attraction.objects.get(pk=request.data["attraction_id"])
        customer = Customer.objects.get(user=request.auth.user)
     
        newitinerary = Itinerary()
        newitinerary.starttime = request.data["starttime"]
        newitinerary.attraction_id = request.data["attraction_id"]
        newitinerary.customer_id = request.data["customer_id"]
        newitinerary.save()

        serializer = ItinerarySerializer(newitinerary, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            serializer = ItinerarySerializer(itinerary, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        itinerary = Itinerary.objects.get(pk=pk)
        itinerary.starttime = request.data["starttime"]
        itinerary.attraction_id = request.data["attraction_id"]
        itinerary.customer_id = request.data["customer_id"]
        itinerary.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            itinerary.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        # customer = Customer.objects.get(user=request.auth.user)
        itineraries = Itinerary.objects.all()
        serializer = ItinerarySerializer(
            itineraries, many=True, context={'request': request})
        return Response(serializer.data)