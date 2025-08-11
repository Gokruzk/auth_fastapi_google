import LinkButton from "@/components/LinkButton";

const API_URL = process.env.API_URL;

export default function Home() {
  return (
    <main>
      <div className="px-9 pt-5">Google Auth</div>
      <div className="px-9 py-5">
        <LinkButton
          title="Login"
          href={`${API_URL}/api/v1/auth/login/google`}
          style="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mr-2 rounded"
        />
      </div>
    </main>
  );
}
