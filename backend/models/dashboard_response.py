"""
========================================
Dashboard Response Models
========================================
"""

from typing import List, Optional

from pydantic import BaseModel


# ========================================
# Intelligence Graph
# ========================================

class NodePosition(BaseModel):
    top: Optional[str] = None
    left: Optional[str] = None
    right: Optional[str] = None
    bottom: Optional[str] = None


class GraphNode(BaseModel):
    id: str
    label: str
    value: int | str
    color: str
    position: NodePosition


class GraphLegend(BaseModel):
    id: str
    label: str
    color: str


class GraphStatistics(BaseModel):
    nodes: int
    connections: int
    lastAnalysis: str


class IntelligenceGraphResponse(BaseModel):
    title: str
    subtitle: str
    filterLabel: str
    nodes: List[GraphNode]
    legends: List[GraphLegend]
    statistics: GraphStatistics


# ========================================
# Workspace Health
# ========================================

class WorkspaceMetric(BaseModel):
    id: str
    label: str
    value: str
    progress: int
    icon: str
    color: str


class WorkspaceHealthResponse(BaseModel):
    title: str
    subtitle: str
    status: str
    statusColor: str
    lastUpdated: str
    metrics: List[WorkspaceMetric]


# ========================================
# Active Document
# ========================================

class ActiveDocumentResponse(BaseModel):
    id: str
    title: str
    type: str
    size: str
    updatedAt: str
    summary: str


# ========================================
# Upload & Analyze
# ========================================

class UploadAnalyzeResponse(BaseModel):
    title: str
    acceptedTypes: List[str]
    maxSize: str


# ========================================
# AI Workflows
# ========================================

class AIWorkflowsResponse(BaseModel):
    title: str
    running: int
    completed: int
    failed: int
    queue: int


# ========================================
# Dashboard
# ========================================

class DashboardResponse(BaseModel):
    intelligenceGraph: IntelligenceGraphResponse
    workspaceHealth: WorkspaceHealthResponse
    activeDocument: ActiveDocumentResponse
    uploadAnalyze: UploadAnalyzeResponse
    aiWorkflows: AIWorkflowsResponse