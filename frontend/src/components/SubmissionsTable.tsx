import DownloadSubmission from "./DownloadSubmission";
import Dot from "./Dot";

export interface Submission  {
    id: number;
    bucket: string;
    path: string;
    created_at: string;
    status: string;
}

const SubmissionTable = ({data}: {data: Submission[]}) => {

    const isReady = (status: string) => {
        if (status === 'ready') {
            return true;
        } else return false;
        
    }

    return (
        <div className="bg-white w-full md:col-span-3 relative h-[90vh] m-auto p-4 border rounded-lg">
            <table className="w-full">
                <thead>
                    <tr>
                        <td>ID</td>
                        <td>название</td>
                        <td>Дата создания</td>
                        <td>Статус</td>
                    </tr>
                </thead>
                <tbody>
                    {data.map((submission, index) => (
                    <tr key={index} className="">
                        <td>{submission.id}</td>
                        <td>{submission.path}</td>
                        <td>{submission.created_at}</td>
                        <td> <Dot status={submission.status}/></td>       
                        <td><DownloadSubmission id={submission.id} filename={submission.path} ready={isReady(submission.status)}/></td>         
                    </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

export default SubmissionTable;