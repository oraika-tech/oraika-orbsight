import html2canvas from 'html2canvas';
import { StaticImageData } from 'next/image';
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { jsPDF } from 'jspdf';
import { wrapSentence } from '../utils/common';

export enum PdfMode {
    REPORT,
    SIMPLE
}

async function loadImageData(url: string) {
    const response = await fetch(url);
    const blob = await response.blob();
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
}

export async function handleDownloadPdf(elements: HTMLElement[],
    fileName: string, pdfMode: PdfMode, title: string,
    oraikaLogo: string, tenantLogoOrName: StaticImageData | string, completed: () => void) {
    // eslint-disable-next-line new-cap
    const pdf = new jsPDF('p', 'pt', 'a4');

    const canvases = await Promise.all(elements.map(element => html2canvas(element, {
        backgroundColor: '#F1F3F5'
    })));

    const oraikaLogoImage = await loadImageData(oraikaLogo) as string;
    const tenantLogoImage = typeof tenantLogoOrName === 'string'
        ? tenantLogoOrName
        : await loadImageData(tenantLogoOrName.src) as string;

    // Define margins
    const headingCenterY = pdfMode === PdfMode.REPORT ? 40 : 0;
    const marginX = 20;
    const marginY = 20;

    const totalMarginX = marginX * 2;
    const totalMarginY = pdfMode === PdfMode.REPORT ? headingCenterY + 20 + marginY * 2 : marginY * 2;

    const { pageSize } = pdf.internal;
    const pageAspactRatio = (pageSize.getHeight() - totalMarginY) / (pageSize.getWidth() - totalMarginX);

    for (let i = 0; i < canvases.length; i += 1) {
        const canvas = canvases[i];
        const data = canvas.toDataURL('image/jpeg');

        if (pdfMode === PdfMode.REPORT) {
            pdf.setTextColor('blue');
            pdf.setFont('Helvetica', 'bold');

            let yPosition = 10;
            let reportTitle = title;
            let fontSize = 21;
            if (title.length > 26) {
                const lines = wrapSentence(title, 34);
                reportTitle = lines.join('\n');
                yPosition = lines.length >= 3 ? -13 : 0;
                fontSize = 18;
            }
            pdf.setFontSize(fontSize);
            pdf.text(reportTitle,
                (pageSize.getWidth() / 2) - marginX - 20,
                headingCenterY + yPosition,
                { align: 'center' });

            pdf.addImage(oraikaLogoImage, 'JPEG', marginX + 415, headingCenterY - 21, 150, 42);
            if (typeof tenantLogoOrName === 'string') {
                pdf.setTextColor('black');
                pdf.text(tenantLogoOrName, marginX, headingCenterY + yPosition);
            } else {
                const width = 60;
                const height = Math.round((width * tenantLogoOrName.height) / tenantLogoOrName.width);
                pdf.addImage(tenantLogoImage, 'JPEG', marginX, headingCenterY - (height / 2), width, height);
            }
        }

        // eslint-disable-next-line new-cap
        const imgProperties = pdf.getImageProperties(data);
        let pdfHeight = 0;
        let pdfWidth = 0;
        let x = 0;
        const y = totalMarginY - marginY; // total - bottom margin => header + margin

        // Checking which side of image is bigger w.r.t paper size.
        // Comparing page aspact ratio with image aspect ratio
        if ((imgProperties.height / imgProperties.width) > pageAspactRatio) {
            pdfHeight = pageSize.getHeight() - totalMarginY;
            pdfWidth = (imgProperties.width * pdfHeight) / imgProperties.height;
            x = (pdf.internal.pageSize.getWidth() - pdfWidth) / 2;
        } else {
            pdfWidth = pageSize.getWidth() - totalMarginX;
            pdfHeight = (imgProperties.height * pdfWidth) / imgProperties.width;
            x = marginX;
        }

        pdf.addImage(data, 'JPEG', x, y, pdfWidth, pdfHeight);
        if (i < canvases.length - 1) {
            pdf.addPage();
        }
    }
    pdf.save(fileName);
    completed();
}
