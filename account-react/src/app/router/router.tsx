import { useMemo } from "react";
import AppRoot, { ErrorBoundary } from "@/app/routes/app/root";
import { paths } from "@/config/paths";

import { QueryClient, useQueryClient } from "@tanstack/react-query";
import { createBrowserRouter } from "react-router";
import { RouterProvider } from "react-router-dom";
import { Spinner } from "@/components/ui/spinner";

const convert = (queryClient: QueryClient) =>(m : any) =>{
    const { clientLoader, clientAction, default: Component, ...rest } = m;
    return {
        ...rest,
        loder: clientLoader?.(queryClient),
        action: clientAction?.(queryClient),
        Component,
    };
};
