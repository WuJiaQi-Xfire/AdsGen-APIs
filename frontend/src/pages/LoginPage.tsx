import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/UI/PrimaryButton";
import { Input } from "@/components/UI/Input";
import { Label } from "@/components/UI/Label";
import { AuthLayout } from "./AuthLayout";
import { loginUser } from "@/lib/api/auth";

export function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    const result = await loginUser(email, password);
    
    if (!result.error) {
      localStorage.setItem('authToken', result.token);
      navigate("/");
    } else {
      alert(result.message);
    }
    
    setIsLoading(false);
  };

  return (
    <AuthLayout
      title="Sign in to your account"
      subtitle="Don't have an account?"
      linkText="Sign up"
      linkUrl="/signup"
    >
      <form className="space-y-6" onSubmit={handleSubmit}>
        <div>
          <Label htmlFor="email">Email address</Label>
          <Input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1"
          />
        </div>

        <div>
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1"
          />
        </div>

        <div className="flex items-center justify-end">
          <Link
            to="/forgot-password"
            className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
          >
            Forgot your password?
          </Link>
        </div>

        <div>
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Signing in..." : "Sign in"}
          </Button>
        </div>
      </form>
    </AuthLayout>
  );
}
