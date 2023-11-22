// getHeadings credit: Josh W. Comeau
export function getHeadings(source: string) {
    const headingLines = source.split('\n').filter((line) => line.match(/^###*\s/));

    function getHeadingLevel(line: string) {
        let level = 0;
        for (let i = 0; i < line.length; i += 1) {
            if (line[i] === '#') {
                level += 1;
            } else {
                break;
            }
        }
        return level;
    }

    return headingLines.map((raw) => {
        const level = getHeadingLevel(raw);
        const text = raw.replace(/^###*\s/, '');

        return { text, level };
    });
}

export function getHeadingAnchor(title: string) {
    return title
        .toLowerCase()
        .replace('/', '')
        .replace(/ /g, '-')
        .replace(/[^a-z0-9-]/g, '');
}
