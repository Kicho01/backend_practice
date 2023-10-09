from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
#
#implementacion del ejercicio
#
@api_view(['POST'])
def get_data(request):
  data = request.data
  result = process_orders(data.get('orders'), data.get('criterion'))
  if type(result) == str:
    return Response({"error": result})
  return Response({"total": result})


def process_orders(orders, criterion):
    total = 0
    error = "Error: Invalid Price Format"

    for order in orders:
        if order["price"] < 0:
            return error
        if criterion == 'completed':
            if order['status'] == 'completed':
                total += order['price'] * order['quantity']
        elif criterion == 'canceled':
            if order['status'] == 'canceled':
                total += order['price'] * order['quantity']
        elif criterion == 'pending':
            if order['status'] == 'pending':
                total += order['price'] * order['quantity']
        elif criterion == 'all':
            total += order['price'] * order['quantity']
    return total