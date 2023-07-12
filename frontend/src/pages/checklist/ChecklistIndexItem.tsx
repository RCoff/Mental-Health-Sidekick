import {useState, useEffect} from 'react';
import {Button, Badge, Flex, Space, Group, Box, Text} from "@mantine/core";

import styles from "./Checklist.module.css"

interface Props {
    text: string;
    id: string;
    index: number;
    total_items: number;
    completed_items: number;
    onClick?: () => void;
}

export const ChecklistIndexItem = ({text, id, index, total_items, completed_items, onClick}: Props) => {
    const handleOnClick = () => {
        if (onClick) onClick()
    }

    return (
        <Box
            display="flex"
            id={id}
            key={index}
            sx={(theme) => ({
                border: "0.0625rem solid",
                borderColor: theme.colors.dark[0],
                borderRadius: theme.radius.sm,
                justifyContent: "space-between",
                '&:hover': {
                    backgroundColor: theme.colors.gray[1]
                }
            })}
            pl={18}
            pr={18}
            mih={55}
            miw={450}
            onClick={handleOnClick}
        >
            <Text
                fz="xl"
                fw={600}
                color={"black"}
                style={{display: "flex", alignItems: "center"}}
            >
                {text}
            </Text>
            <Group
                position="right"
                align="flex-start"
                spacing="xs"
                style={{marginTop: "0.5rem"}}
            >
                <Badge
                    variant="filled"
                    title="Total items"
                >
                    {total_items}
                </Badge>
                <Badge
                    variant="filled"
                    color="green"
                    title="Completed items"
                >
                    {completed_items}
                </Badge>
            </Group>
        </Box>
    );
};