from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from reviews.models import ReviewTeacher
import uuid

class ReviewViewsTests(APITestCase):
    
    def setUp(self):
        self.student = User.objects.create_user(username="student", password="pass123")
        self.teacher = User.objects.create_user(username="teacher", password="pass123")
        self.other_user = User.objects.create_user(username="intruder", password="pass123")
  
        self.review = ReviewTeacher.objects.create(
            student=self.student,
            teacher=self.teacher,
            score=5,
            comment="Great teacher!"
        )
        self.client.force_authenticate(user=self.student)

    # Testes de criação

    def test_create_review_successfully_persists_data(self):
        self.review.delete()
        # Arrange
        # Usa reverse para pegar a URL correta: /professor/<pk>/avaliar/
        url = reverse('review-create', kwargs={'pk': self.teacher.pk})
        data = {"score": 4, "comment": "Good class"}
        
        # Act
        response = self.client.post(url, data)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ReviewTeacher.objects.filter(comment="Good class").exists())
        
        created_review = ReviewTeacher.objects.get(comment="Good class")
        self.assertEqual(created_review.student, self.student)
        self.assertEqual(created_review.teacher, self.teacher)

    def test_create_review_fails_when_unauthenticated(self):
        # Arrange
        self.client.logout()
        url = reverse('review-create', kwargs={'pk': self.teacher.pk})
        data = {"score": 4, "comment": "Anonymous review"}
        
        # Act
        response = self.client.post(url, data)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_review_raises_404_for_missing_teacher(self):
        # Arrange
        missing_id = uuid.uuid4()
        url = reverse('review-create', kwargs={'pk': missing_id})
        data = {"score": 3, "comment": "Ghost teacher"}
        
        # Act
        response = self.client.post(url, data)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_review_fails_with_invalid_data(self):
        # Arrange
        url = reverse('review-create', kwargs={'pk': self.teacher.pk})
        data = {"score": 10000} 
        
        # Act
        response = self.client.post(url, data)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testes de atualização

    def test_update_review_modifies_fields_successfully(self):
        # Arrange
        url = reverse('review-update', kwargs={'pk': self.review.pk})
        data = {"score": 3, "comment": "Updated comment"}
        
        # Act
        response = self.client.put(url, data)
        
        # Assert
        self.review.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.review.comment, "Updated comment")
        self.assertEqual(self.review.score, 3)

    def test_update_review_forbidden_for_non_author(self):
        # Arrange
        self.client.force_authenticate(user=self.other_user) 
        url = reverse('review-update', kwargs={'pk': self.review.pk})
        data = {"score": 5, "comment": "Hacked comment"}
        
        # Act
        response = self.client.put(url, data)
        
        # Assert
        self.review.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.review.comment, "Hacked comment")

    # Teste de deleção

    def test_delete_review_removes_instance_from_db(self):
        # Arrange
        url = reverse('review-delete', kwargs={'pk': self.review.pk})
        
        # Act
        response = self.client.delete(url)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ReviewTeacher.objects.filter(pk=self.review.pk).exists())

    def test_delete_review_forbidden_for_non_author(self):
        # Arrange
        self.client.force_authenticate(user=self.other_user)
        url = reverse('review-delete', kwargs={'pk': self.review.pk})
        
        # Act
        response = self.client.delete(url)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(ReviewTeacher.objects.filter(pk=self.review.pk).exists())

    # Testes de listagem

    def test_get_all_reviews_returns_descending_order(self):
        # Arrange
        other_student = User.objects.create_user(username="student2", password="123")
               
        new_review_in_test = ReviewTeacher.objects.create(
            student=other_student, teacher=self.teacher, score=1, comment="Newer"
        )
        
        url = reverse('review-list-all')
        
        # Act
        response = self.client.get(url)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        
        self.assertEqual(results[0]['id'], str(new_review_in_test.id))
        self.assertEqual(results[1]['id'], str(self.review.id))
        
    def test_get_reviews_by_professor_filters_correctly(self):
        # Arrange
        other_teacher = User.objects.create_user(username="other_prof", password="123")
        
        ReviewTeacher.objects.create(student=self.student, teacher=other_teacher, score=5)
        
        url = reverse('review-list-professor', kwargs={'pk': self.teacher.pk})
        
        # Act
        response = self.client.get(url)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], str(self.review.id))

    # Testes de detalhes

    def test_get_professor_detail_returns_correct_user(self):
        # Arrange
        url = reverse('teacher-detail', kwargs={'pk': self.teacher.pk})
        
        # Act
        response = self.client.get(url)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.teacher.username)

    def test_get_professor_detail_raises_404_for_missing_id(self):
        # Arrange
        missing_id = uuid.uuid4()
        url = reverse('teacher-detail', kwargs={'pk': missing_id})
        
        # Act
        response = self.client.get(url)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)