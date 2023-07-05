import {useState, useEffect} from 'react';

import {
    Stack,
    Button,
    Container
} from '@mantine/core';

import {Checklist} from "../../api/models.ts";
import {getChecklists} from "../../api";
// import styles from "./ChecklistList.module.css"

const ChecklistList = () => {
    const [error, setError] = useState<unknown>()
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [checklistListItems, setChecklistListItems] = useState<Checklist[]>([]);

    const doGetChecklists = async () => {
        error && setError(undefined);
        setIsLoading(true)

        try {
            const checklists = await getChecklists();
            setChecklistListItems(checklists.checklists)
        } catch (e) {
            setError(e);
        } finally {
            setIsLoading(false)
        }
    };

    useEffect(() => {
        void doGetChecklists();
    }, []);

    return (
        <Container size="xs" px="xs">
            <h1>Test2</h1>
            <Stack>
                {!isLoading && checklistListItems.map((checklist, index) => (
                    <Button key={index} variant="outline">{checklist.name}</Button>
                ))}
                <Button
                    variant="outline"
                    onClick={doGetChecklists}
                >Test</Button>
            </Stack>
            <Button variant="outline">+</Button>
        </Container>
    );
};

export default ChecklistList;