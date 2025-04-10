import { useLocation } from "react-router-dom";
import { useEffect } from "react";
import { FileX } from "lucide-react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
  }, [location.pathname]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <div className="text-center bg-white p-10 rounded-xl shadow-sm border border-gray-100 max-w-md animate-fade-in">
        <div className="mb-6 flex justify-center">
          <div className="rounded-full bg-gray-100 p-3">
            <FileX className="h-10 w-10 text-brand-red" />
          </div>
        </div>
        <h1 className="text-3xl font-semibold mb-2">404</h1>
        <p className="text-lg text-gray-600 mb-6">
          The page you're looking for can't be found
        </p>
        <a href="/" className="primary-button inline-block">
          Return to Home
        </a>
      </div>
    </div>
  );
};

export default NotFound;
