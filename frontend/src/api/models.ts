export type Checklist = {
    id: string;
    name: string;
    description?: string;
    created_datetime?: string;
    modified_datetime?: string;
}

export type ChecklistItem = {
    id: string;
    text: string;
    created_datetime?: string;
    modified_datetime?: string;
}

export type ChecklistResponse = {
    checklists: Checklist[];
}

export type ChecklistItemResponse = {
    checklist_items: ChecklistItem[];
    checklist_name: string;
}