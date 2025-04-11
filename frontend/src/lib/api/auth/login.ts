import apiClient from '../apiClient';
import { handleApiError } from '../errorHandler';

export const loginUser = async (email: string, password: string) => {
  try {
    const response = await apiClient.post('/auth/login', { email, password });
    return response.data;
  } catch (error) {
    return handleApiError(error, 'Failed to login');
  }
};
