import {ChangeEvent} from "react";
import {useEffect, useState} from "react";
import {Button, Container, Stack, Box, Text, Checkbox, Card} from "@mantine/core";
import {updateChecklistItem} from "../../api";


interface Props {
    id: string;
    index: number;
    text?: string;
    defaultValue: boolean;
}


export const ChecklistItem = ({id, index, text, defaultValue}: Props) => {
    const [checked, setChecked] = useState<boolean>(defaultValue)
    const [updateChecked, setUpdateChecked] = useState<boolean>(defaultValue)
    const [updating, setUpdating] = useState<boolean>(false)

    const handleCheckChange = (_ev?: React.ChangeEvent<HTMLInputElement>) => {
        setUpdating(true)
        setUpdateChecked(checked)
        setChecked(!checked)

        try {
            void updateChecklistItem(id)
        } catch (e) {
            console.error(e)
            setChecked(updateChecked)
        } finally {
            setUpdating(false)
        }
    }

    return (
        <Box
            id={id}
            key={index}
            display="flex"
            style={{alignItems: "center"}}
        >
            <Checkbox
                checked={checked}
                size="sm"
                label={text}
                onChange={handleCheckChange}
            />
        </Box>
    )
}