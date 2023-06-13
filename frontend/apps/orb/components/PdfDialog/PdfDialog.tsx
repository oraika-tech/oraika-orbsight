import { Button, Group, SegmentedControl, Stack, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';
import { PdfMode } from 'common-utils/service/pdf-service';
import { useState } from 'react';

interface PdfDialogProps {
    fileName: string
    title: string
    close: () => void
    generatePdf: (fileName: string, pdfMode: PdfMode, title?: string) => void
}

export default function PdfDialog({ fileName, title, close, generatePdf }: PdfDialogProps) {
    const [isSubmitting, setSubmitting] = useState(false);
    const form = useForm({
        initialValues: {
            fileName,
            title,
            pdfMode: PdfMode.REPORT.toString()
        },
        validate: {
            fileName: (value) => (value.length > 0 ? null : 'Please fill pdf file name'),
            title: (value, values) => (values.pdfMode !== PdfMode.REPORT.toString() || value.length > 0
                ? null : 'Please fill report title')
        }
    });

    const handlePdfDownload = async (values) => {
        const enumValue: PdfMode = values.pdfMode === PdfMode.REPORT.toString() ? PdfMode.REPORT : PdfMode.SIMPLE;
        generatePdf(values.fileName, enumValue, values.title);
    };

    return (
        <form
            onSubmit={(event) => {
                setSubmitting(true);
                event.preventDefault();
                form.onSubmit(handlePdfDownload)(event);
            }}
        >
            <Stack spacing="md" p="xs">
                <SegmentedControl
                    data={[
                        { label: 'Report', value: PdfMode.REPORT.toString() },
                        { label: 'Simple', value: PdfMode.SIMPLE.toString() }
                    ]}
                    {...form.getInputProps('pdfMode')}
                />
                <TextInput label="File Name" {...form.getInputProps('fileName')} />
                {form.values.pdfMode === PdfMode.REPORT.toString() && (
                    <TextInput label="Report Title" {...form.getInputProps('title')} />
                )}
                <Group p="xl" position="apart">
                    <Button
                        w={120}
                        radius="md"
                        variant="outline"
                        size="md"
                        onClick={close}
                    >
                        Cancel
                    </Button>
                    <Button
                        w={120}
                        radius="md"
                        variant="filled"
                        size="md"
                        type="submit"
                        loading={isSubmitting}
                    >
                        OK
                    </Button>
                </Group>
            </Stack>
        </form>
    );
}
