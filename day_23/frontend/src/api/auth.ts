import api from "./client";
import type {
  RegisterRequest,
  LoginRequest,
  LoginResponse,
} from "../types/auth";

export async function register(data: RegisterRequest) {
  console.log(data);
  const response = await api.post(
    "/auth/register",
    data
  );

  return response.data;
}

export async function login(
  data: LoginRequest
): Promise<LoginResponse> {
  console.log(data);
  const response = await api.post<LoginResponse>(
    "/auth/login",
    data
  );

  console.log(response)

  return response.data;
}