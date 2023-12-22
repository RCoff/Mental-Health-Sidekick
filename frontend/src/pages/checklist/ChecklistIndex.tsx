import {useState, useEffect} from 'react';
import {Routes, Route, Link, Outlet} from 'react-router-dom';

import {
    Stack,
    Button,
    Container
} from '@mantine/core';

import {ChecklistIndexItem as IndexItem} from "./ChecklistIndexItem"
import {
    getChecklistIndex,
    ChecklistIndexItem
} from "../../api";

import styles from "./Checklist.module.css"

const ChecklistIndex = () => {
    const [error, setError] = useState<unknown>()
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [checklistListItems, setChecklistListItems] = useState<ChecklistIndexItem[]>([]);

    const doGetChecklists = async () => {
        error && setError(undefined);
        setIsLoading(true)

        try {
            const checklists = await getChecklistIndex();
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
            <Button
                mt={"3rem"}
                w={"6rem"}
                variant="outline"
                radius="sm"
                onClick={doGetChecklists}
            >+ New</Button>
            <Stack mt={"1.5rem"}>
                {!isLoading && checklistListItems.map((checklist, index) => (
                    // <Button key={index} variant="outline">{checklist.name}</Button>
                    <Link to={checklist.id} className={styles.checklistIndexItemLink}>
                        <IndexItem
                            index={index}
                            id={checklist.id}
                            text={checklist.name}
                            total_items={checklist.item_count}
                            completed_items={checklist.checked_item_count}
                        />
                    </Link>
                ))}
            </Stack>
        </Container>
    );
};

export default ChecklistIndex;