import {useParams, Link, useNavigate} from "react-router-dom"
import {getChecklist} from "../../api";
import {useEffect, useState} from "react";

import {Button, Container, Stack} from "@mantine/core";

import {ChecklistItem} from "../../api";

type params = {
    id: string;
}

const Checklist = () => {
    const {id} = useParams<params>();
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [checklistName, setChecklistName] = useState<string>("")
    const [checklistItems, setChecklistItems] = useState<ChecklistItem[]>([])

    const doGetChecklist = async () => {
        if (!id) return;

        setIsLoading(true);
        try {
            const checklist = await getChecklist(id)
            setChecklistItems(checklist.checklist_items)
            setChecklistName(checklist.checklist_name)
        } catch (e) {
            console.log(e)
        } finally {
            setIsLoading(false);
        }
    }

    useEffect(() => {
        void doGetChecklist();
    }, [id])

    return (
        <Container size="xs" px="xs">
            <Button
                mt={"3rem"}
                w={"6rem"}
                variant={"outline"}
                radius="sm"
                onClick={() => navigate(-1)}>{"< Back"}</Button>
            <h1>{checklistName}</h1>
            <Stack>
                {!isLoading && checklistItems.map((item, index) => (
                    <li key={index}>
                        <p>{item.text}</p>
                    </li>
                ))}
            </Stack>
        </Container>
    )
}

export default Checklist;