import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const appAPI = axios.create({
  baseURL: API_URL,
});

export const authUser = async () => {
  try {
    const res = await appAPI.get("api/v1/auth/login/google");
    if (res.status === 200) {
      const data = res.data.result.token;
      return { status: res.status, data: data };
    } else {
      return { status: res.status, error: "F" };
    }
  } catch (error: any) {
    console.log(error);
    return { status: 500, error: "F" };
  }
};
