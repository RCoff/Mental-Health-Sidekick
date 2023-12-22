import {
    ChecklistIndexResponse,
    ChecklistResponse,
    GenericResponse,
    ChecklistItem,
    ChecklistItemResponse,
    UpdateChecklistItemRequest
} from "./models.ts";

export async function getChecklistIndex(): Promise<ChecklistIndexResponse> {
    const response = await fetch("/checklist-api", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });

    const parsedResponse: ChecklistIndexResponse = await response.json()
    if (response.status > 299 || !response.ok) {
        throw Error("Error")
    }

    return parsedResponse;
}

export async function getChecklist(checklist_id: string): Promise<ChecklistResponse> {
    const response = await fetch("/checklist-api/" + checklist_id, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });

    const parsedResponse: ChecklistResponse = await response.json()
    if (response.status > 299 || !response.ok) {
        throw Error("Error")
    }

    return parsedResponse;
}

export async function addChecklistItem(checklist_id: string): Promise<ChecklistItemResponse> {
    const response = await fetch("/checklist-api/" + checklist_id + "/item", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    });

    const parsedResponse: ChecklistItemResponse = await response.json()
    if (response.status > 299 || !response.ok) {
        throw Error(await response.text())
    }

    return parsedResponse
}

export async function updateChecklistItem(checklist_item_id: string, status: boolean, text: string): Promise<GenericResponse> {
    const response = await fetch("/checklist-api/item/" + checklist_item_id, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"status": status})
    });

    const parsedResponse: GenericResponse = await response.json()
    if (response.status > 299 || !response.ok) {
        throw Error(await response.text())
    }

    return parsedResponse
}