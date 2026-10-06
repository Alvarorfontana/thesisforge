import Sidebar from "@/components/layout/Sidebar";
import TopBar from "@/components/layout/TopBar";
import ModuleBuilder from "@/components/thesis/ModuleBuilder";

export default function Dashboard() {
  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />
      <main className="flex-1 p-6">
        <TopBar />
        <ModuleBuilder />
      </main>
    </div>
  );
}
