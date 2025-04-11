import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/UI/PrimaryButton";
import { Input } from "@/components/UI/Input";
import { Label } from "@/components/UI/Label";
import { AuthLayout } from "./AuthLayout";
import { signupUser } from "@/lib/api/auth";

export function SignupPage() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      alert("Passwords don't match");
      return;
    }

    setIsLoading(true);
    
    const result = await signupUser({
      email, 
      username,
      full_name: fullName,
      password 
    });

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
      title="Create a new account"
      subtitle="Already have an account?"
      linkText="Sign in"
      linkUrl="/login"
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
          <Label htmlFor="username">Username</Label>
          <Input
            id="username"
            name="username"
            type="text"
            autoComplete="username"
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="mt-1"
          />
        </div>

        <div>
          <Label htmlFor="fullName">Full Name (Optional)</Label>
          <Input
            id="fullName"
            name="fullName"
            type="text"
            autoComplete="name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            className="mt-1"
          />
        </div>

        <div>
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            name="password"
            type="password"
            autoComplete="new-password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1"
          />
        </div>

        <div>
          <Label htmlFor="confirmPassword">Confirm Password</Label>
          <Input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            autoComplete="new-password"
            required
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="mt-1"
          />
        </div>

        <div>
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Creating account..." : "Create account"}
          </Button>
        </div>
      </form>
    </AuthLayout>
  );
}
