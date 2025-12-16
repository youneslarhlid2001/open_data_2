import React, { useMemo } from "react";
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
} from "@tanstack/react-table";

const columnsDef = [
  { accessorKey: "code", header: "Code" },
  { accessorKey: "product_name", header: "Produit" },
  { accessorKey: "brands", header: "Marques" },
  { accessorKey: "nutriscore_grade", header: "Nutri-Score" },
  { accessorKey: "nova_group", header: "NOVA" },
  { accessorKey: "energy_100g", header: "Énergie/100g" },
  { accessorKey: "fat_100g", header: "Gras/100g" },
  { accessorKey: "sugars_100g", header: "Sucres/100g" },
  { accessorKey: "salt_100g", header: "Sel/100g" },
  { accessorKey: "proteins_100g", header: "Protéines/100g" },
];

export default function DataTable({ data = [] }) {
  const columns = useMemo(() => columnsDef, []);

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="table-container">
      <table>
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th key={header.id}>
                  {flexRender(header.column.columnDef.header, header.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

