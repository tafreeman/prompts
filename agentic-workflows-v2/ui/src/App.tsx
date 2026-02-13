import { Routes, Route, Navigate } from "react-router-dom";
import { lazy, Suspense } from "react";
import Sidebar from "./components/layout/Sidebar";
import ErrorBoundary from "./components/common/ErrorBoundary";

// Code-split pages for better initial load performance
const DashboardPage = lazy(() => import("./pages/DashboardPage"));
const WorkflowsPage = lazy(() => import("./pages/WorkflowsPage"));
const WorkflowDetailPage = lazy(() => import("./pages/WorkflowDetailPage"));
const RunDetailPage = lazy(() => import("./pages/RunDetailPage"));
const LivePage = lazy(() => import("./pages/LivePage"));

function PageLoader() {
  return (
    <div className="flex h-full items-center justify-center text-gray-400">
      <div className="animate-pulse">Loading...</div>
    </div>
  );
}

export default function App() {
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <Suspense fallback={<PageLoader />}>
          <Routes>
            <Route path="/" element={<ErrorBoundary><DashboardPage /></ErrorBoundary>} />
            <Route path="/workflows" element={<ErrorBoundary><WorkflowsPage /></ErrorBoundary>} />
            <Route path="/workflows/:name" element={<ErrorBoundary><WorkflowDetailPage /></ErrorBoundary>} />
            <Route path="/runs/:filename" element={<ErrorBoundary><RunDetailPage /></ErrorBoundary>} />
            <Route path="/live/:runId" element={<ErrorBoundary><LivePage /></ErrorBoundary>} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Suspense>
      </main>
    </div>
  );
}
