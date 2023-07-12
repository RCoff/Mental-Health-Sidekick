import {useState, useEffect} from 'react';
import {Button, Badge, Flex, Space, Group} from "@mantine/core";

import styles from "./ChecklistIndex.module.css"

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
        <Button
            display="flex"
            id={id}
            key={index}
            variant="outline"
            color="gray"
            radius="sm"
            pl={18}
            pr={18}
            mih={55}
            miw={450}
            onClick={handleOnClick}
            styles={(theme) => ({
                root: {
                    display: "flex",
                    backgroundColor: "rgb(0, 0, 0, 0)",
                    borderColor: "rgba(0, 0, 0, 0.250)"
                },
                label: {
                    color: "rgb(33, 37, 41)",
                    fontWeight: 500,
                    fontSize: "1.25rem"
                }
            })}
        >
            <Group position={"apart"}>
                <Flex
                    pt={8}
                    pb={8}
                >
                    {text}
                </Flex>
                <Group
                    position={"right"}
                    align="flex-start"
                    // gap="xs"
                    // direction="row"
                    // style={{width: "100%"}}
                >
                    <Badge>
                        {total_items}
                    </Badge>
                    <Badge
                        color="green">
                        {completed_items}
                    </Badge>
                </Group>
            </Group>
        </Button>
    );
};