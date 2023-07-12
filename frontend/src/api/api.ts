import {ChecklistResponse, ChecklistItemResponse} from "./models.ts";

export async function getChecklistIndex(): Promise<ChecklistResponse> {
    const response = await fetch("/checklist-api", {
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

export async function getChecklist(checklist_id: string): Promise<ChecklistItemResponse> {
    const response = await fetch("/checklist-api/" + checklist_id, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });

    const parsedResponse: ChecklistItemResponse = await response.json()
    if (response.status > 299 || !response.ok) {
        throw Error("Error")
    }

    return parsedResponse;
}