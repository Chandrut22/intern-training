import { useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { register } from "../api/auth";

export default function RegisterPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  async function handleRegister() {
    try {
      await register({
        username,
        email,
        password,
      });

      navigate({
        to: "/login",
      });
    } catch (err) {
      console.error(err);
      alert("Registration Failed");
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="w-full max-w-md rounded-lg bg-white p-8 shadow-lg">
        <h2 className="mb-6 text-center text-3xl font-bold text-gray-800">
          Register
        </h2>

        <div className="space-y-4">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-4 py-2 outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500"
          />

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-4 py-2 outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500"
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-4 py-2 outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500"
          />

          <button
            onClick={handleRegister}
            className="w-full rounded-md bg-green-600 py-2 font-medium text-white transition hover:bg-green-700"
          >
            Register
          </button>
        </div>
      </div>
    </div>
  );
}