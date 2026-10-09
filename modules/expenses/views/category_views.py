from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import PER_PAGE
from modules.expenses.services import CategoryService

class CategoryListCreateView(APIView):
    def get(self, request):
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", PER_PAGE))
        if page < 1 or limit < 1:
            return Response({"status": 0, "message": "Page or Limit must be a positive integer"}, HTTPStatus.BAD_REQUEST)

        data = CategoryService().findAll(limit=limit, page=page)
        return Response(
            {
                "message": "Category created successfully",
                "data": data,
            },
            status=HTTPStatus.OK,
        )

    def post(self, request):
        data = request.data
        category_id = CategoryService().create(data)

        return Response(
            {
                "message": "Category created successfully",
                "id": category_id,
            },
            status=HTTPStatus.CREATED,
        )

class CategoryDetailView(APIView):
    def get(self, request, pk):
        category_service = CategoryService().find(pk)
        if len(category_service) == 0:
            return Response({"status": 0, "message": "Category not found"}, HTTPStatus.NOT_FOUND)

        return Response({'status': 1, 'message': 'Category found successfully', 'data': category_service}, HTTPStatus.OK)

    def put(self, request, pk):
        data = request.data
        category_service = CategoryService().find(pk)
        if len(category_service) == 0:
            return Response({"status": 0, "message": "Category not found"}, HTTPStatus.NOT_FOUND)
        CategoryService().update(pk, data)
        return Response({'status': 1, 'message': 'Category updated successfully'}, HTTPStatus.OK)

    def delete(self, request, pk):
        category_service = CategoryService().find(pk)
        if len(category_service) == 0:
            return Response({"status": 0, "message": "Category not found"}, HTTPStatus.NOT_FOUND)
        CategoryService().delete(pk)
        return Response({'status': 1, 'message': 'Category deleted successfully'}, HTTPStatus.OK)

