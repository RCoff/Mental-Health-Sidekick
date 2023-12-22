import {useParams, Link, useNavigate} from "react-router-dom"
import {getChecklist} from "../../api";
import {useEffect, useState} from "react";

import {Button, Container, Stack, Box, Text, Checkbox, Card} from "@mantine/core";

import {ChecklistItem as Item} from "./ChecklistItem.tsx";
import {
    addChecklistItem,
    ChecklistItem
} from "../../api";

type params = {
    id: string;
}

const Checklist = () => {
    const {id} = useParams<params>();
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [addingItem, setAddingItem] = useState<boolean>(false);
    const [checklistName, setChecklistName] = useState<string>("")
    const [checklistItems, setChecklistItems] = useState<ChecklistItem[]>([])
    const [editingItemId, setEditingItemId] = useState<string>()

    const doGetChecklist = async () => {
        if (!id) return;

        setIsLoading(true);
        try {
            const checklist = await getChecklist(id)
            setChecklistItems(checklist.checklist_items)
            setChecklistName(checklist.checklist_name)
        } catch (e) {
            console.error(e)
        } finally {
            setIsLoading(false);
        }
    }

    const doAddChecklistItem = async () => {
        if (!id) return;
        if (addingItem) return;

        setAddingItem(true)
        try {
            const addItemResponse = await addChecklistItem(id)
            setChecklistItems([...checklistItems, addItemResponse.checklistItem])
        } catch (e) {
            console.error(e)
        } finally {
            setAddingItem(false)
        }
    }

    useEffect(() => {
        void doGetChecklist();
    }, [id])

    return (
        <Container size="xs" px="xs">
            <div style={{display: "flex", alignItems: "center", marginTop: "3rem"}}>
                <Button
                    w={"6rem"}
                    variant={"outline"}
                    radius="sm"
                    onClick={() => navigate(-1)}>{"< Back"}</Button>
                <div style={{width: "100%", display: "flex", justifyContent: "center"}}>
                    <Text fw="600" fz="2rem">{checklistName}</Text>
                </div>
            </div>
            <Card
                mt="2rem"
                shadow="sm"
                radius="md"
                padding="lg"
                withBorder
            >
                <Stack>
                    {!isLoading && checklistItems.length === 0 && (
                        <Button>Add an item!</Button>
                    )}
                    {!isLoading && checklistItems.map((item, index) => (
                        <Item
                            id={item.id}
                            index={index}
                            defaultValue={item.status}
                            text={item.text}
                        />
                    ))}
                </Stack>
            </Card>
            <div style={{marginTop: "1rem", display: "flex", justifyContent: "flex-end"}}>
                <Button
                    variant="outline"
                    color="gray"
                    radius="sm"
                    onClick={doAddChecklistItem}
                >+ New Item</Button>
            </div>
        </Container>
    )
}

export default Checklist;