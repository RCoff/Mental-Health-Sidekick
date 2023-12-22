export type ChecklistIndexItem = {
    id: string;
    name: string;
    item_count: number;
    checked_item_count: number;
    description?: string;
    created_datetime?: string;
    modified_datetime?: string;
}

export type ChecklistIndexResponse = {
    checklists: ChecklistIndexItem[];
}

export type ChecklistItem = {
    id: string;
    text?: string;
    status: boolean;
    created_datetime?: string;
    modified_datetime?: string;
}

export type ChecklistResponse = {
    checklist_items: ChecklistItem[];
    checklist_name: string;
}

export type ChecklistItemResponse = {
    message: string;
    error?: string;
    checklistItem: ChecklistItem;
}

export type GenericResponse = {
    message?: string;
    error?: string;
}

export type UpdateChecklistItemRequest = {
    status: boolean;
}