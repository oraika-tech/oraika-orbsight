import classes from './CalendlySchedule.module.css';

export default function CalendlySchedule() {
    return (
        <>
            <div
                className={classes.divFrame}
                // className="calendly-inline-widget"
                data-url="https://calendly.com/oraika/15-minute-call?hide_event_type_details=1&hide_gdpr_banner=1"
            />
            <script
                type="text/javascript"
                src="https://assets.calendly.com/assets/external/widget.js"
                async
            />
        </>
    );
}
