"use client";

import { useState } from "react";
import { useDropzone } from "react-dropzone";
import * as XLSX from "xlsx";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";
import { Button } from "~/components/ui/button";

export function Welcome() {
  const [data, setData] = useState<Record<string, any[][]>>({});

  const onDrop = (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    const reader = new FileReader();

    reader.onload = (e) => {
      const binaryStr = e.target?.result;
      const workbook = XLSX.read(binaryStr, { type: "binary" });
    
      const parsedData: Record<string, any[][]> = {};
    
      workbook.SheetNames.forEach((sheetName) => {
        const worksheet = workbook.Sheets[sheetName];
        const sheetJson = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
    
        if (Array.isArray(sheetJson) && sheetJson.length > 0) {
          parsedData[sheetName] = sheetJson as any[][];
        }
      });
    
      setData(parsedData);
    };

    reader.readAsBinaryString(file);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <main className="min-h-screen p-6 bg-muted flex flex-col gap-8">
      {/* Upload de Arquivo */}
      <section {...getRootProps()} className="flex flex-col items-center justify-center border-2 border-dashed rounded-2xl border-primary p-10 bg-background cursor-pointer hover:bg-muted-foreground transition">
        <input {...getInputProps()} />
        <div className="flex flex-col items-center gap-2">
          <p className="text-lg font-semibold text-primary">
            {isDragActive ? "Solte o arquivo aqui..." : "Arraste e solte ou clique para enviar"}
          </p>
          <p className="text-sm text-muted-foreground">Formatos aceitos: .xlsx</p>
          <Button variant="outline" className="mt-4">Selecionar Arquivo</Button>
        </div>
      </section>

      {/* Tabelas */}
      <section className="flex flex-col gap-6">
        {Object.keys(data).length === 0 ? (
          <div className="text-center text-muted-foreground">Nenhum dado carregado ainda.</div>
        ) : (
          Object.keys(data).map((sheetName) => (
            <Card key={sheetName}>
              <CardHeader>
                <CardTitle className="text-primary">{sheetName}</CardTitle>
              </CardHeader>
              <CardContent className="overflow-auto max-h-[400px]">
                <table className="min-w-full text-sm text-left">
                  <thead>
                    <tr>
                      {data[sheetName][0].map((col: any, idx: number) => (
                        <th key={idx} className="px-4 py-2 font-semibold border-b">{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {data[sheetName].slice(1).map((row: any[], rowIndex: number) => (
                      <tr key={rowIndex} className="hover:bg-muted transition">
                        {row.map((cell: any, cellIndex: number) => (
                          <td key={cellIndex} className="px-4 py-2 border-b">
                            {cell}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </CardContent>
            </Card>
          ))
        )}
      </section>
    </main>
  
  );
}
