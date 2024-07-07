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
        <div className="bg-white w-full md:col-span-3 relative h-[90vh] m-auto p-4 border rounded-lg overflow-y-scroll">
            <table className="w-full text-sm text-left rtl:text-right text-gray-500">
                <thead className="text-xs text-gray-700 uppercase bg-gray-50 ">
                    <tr>
                        <td className="px-6 py-3 text-center">ID</td>
                        <td className="px-6 py-3 text-center">название</td>
                        <td className="px-6 py-3 text-center">Дата создания</td>
                        <td className="px-6 py-3 text-center">Статус</td>
                        <td className="px-6 py-3 text-center">Скачать</td>
                    </tr>
                </thead>
                <tbody >
                    {data.slice(0).reverse().map((submission, index) => (
                    <tr key={index} className="bg-white border-b hover:bg-gray-200 ">
                        <td className="px-6 py-4 text-center font-medium text-gray-900 whitespace-nowrap">{submission.id}</td>
                        <td className="px-6 py-4 text-center">{submission.path}</td>
                        <td className="px-6 py-4 text-center">{submission.created_at}</td>
                        <td className="px-6 py-4 grid place-items-center"> <Dot status={submission.status}/></td>       
                        <td className="px-6 py-4 text-center"><DownloadSubmission id={submission.id} filename={submission.path} ready={isReady(submission.status)}/></td>         
                    </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

export default SubmissionTable;