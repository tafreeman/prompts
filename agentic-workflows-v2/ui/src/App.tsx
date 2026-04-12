import { Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/layout/Sidebar";
import DashboardPage from "./pages/DashboardPage";
import WorkflowsPage from "./pages/WorkflowsPage";
import WorkflowDetailPage from "./pages/WorkflowDetailPage";
import WorkflowEditorPage from "./pages/WorkflowEditorPage";
import RunDetailPage from "./pages/RunDetailPage";
import LivePage from "./pages/LivePage";
import { isWorkflowBuilderEnabled } from "./config/featureFlags";

import DatasetsPage from "./pages/DatasetsPage";
import EvaluationsPage from "./pages/EvaluationsPage";

export default function App() {
  const workflowBuilderEnabled = isWorkflowBuilderEnabled();

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-hidden">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/workflows" element={<WorkflowsPage />} />
          {workflowBuilderEnabled && (
            <Route path="/workflows/:name/edit" element={<WorkflowEditorPage />} />
          )}
          <Route path="/workflows/:name" element={<WorkflowDetailPage />} />
          <Route path="/datasets" element={<DatasetsPage />} />
          <Route path="/evaluations" element={<EvaluationsPage />} />
          <Route path="/runs/:filename" element={<RunDetailPage />} />
          <Route path="/live/:runId" element={<LivePage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
