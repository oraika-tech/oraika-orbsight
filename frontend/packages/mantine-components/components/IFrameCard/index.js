import { Card } from "@mantine/core/Card";
import './style.css';

function IFrameCard(props) {
    return (
        <Card style={{ height: "100%" }}>
            <iframe
                style={props.style}
                title={props.title}
                src={props.src}
                srcDoc={props.srcDoc}
                width="100%"
                height="825"
                scrolling="auto"
                align="center"
                className="iframe-ds"
                frameBorder={0}
            >
            </iframe>
        </Card >
    );
}

export default IFrameCard;
