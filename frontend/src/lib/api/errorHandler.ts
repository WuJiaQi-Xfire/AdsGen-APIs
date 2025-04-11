import { AxiosError } from 'axios';

export const handleApiError = (error: unknown, defaultMessage: string) => {
  const axiosError = error as AxiosError;
  
  if (axiosError.response) {
    // Server responded with error status
    return {
      error: true,
      message: axiosError.response.data?.message || defaultMessage,
      status: axiosError.response.status
    };
  } else if (axiosError.request) {
    // Request was made but no response
    return {
      error: true,
      message: 'No response from server',
      status: 0
    };
  } else {
    // Something else happened
    return {
      error: true,
      message: defaultMessage,
      status: 0
    };
  }
};
