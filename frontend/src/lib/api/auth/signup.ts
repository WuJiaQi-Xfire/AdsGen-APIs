import apiClient from '../apiClient';
import { handleApiError } from '../errorHandler';

export const signupUser = async (userData: {
  email: string;
  username: string;
  full_name?: string;
  password: string;
}) => {
  try {
    const response = await apiClient.post('/auth/signup', userData);
    return response.data;
  } catch (error) {
    return handleApiError(error, 'Failed to sign up');
  }
};
