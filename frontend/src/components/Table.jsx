export default function Table({ data }) {
  if (!data || data.length === 0) {
    return <div className="mt-4 text-gray-600">No results found.</div>;
  }

  return (
    <div className="mt-4 overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Android
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Desktop
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              City
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Country
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Email
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              First Name
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              iPhone
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              ID
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Phone
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Surname
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((person) => (
            <tr key={person.id}>
              <td className="px-6 py-4 whitespace-nowrap">
                {person.Android.toString()}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                {person.Desktop.toString()}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">{person.city}</td>
              <td className="px-6 py-4 whitespace-nowrap">{person.country}</td>
              <td className="px-6 py-4 whitespace-nowrap">{person.email}</td>
              <td className="px-6 py-4 whitespace-nowrap">
                {person.firstName}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                {person.iPhone.toString()}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">{person.id}</td>
              <td className="px-6 py-4 whitespace-nowrap">{person.phone}</td>
              <td className="px-6 py-4 whitespace-nowrap">{person.surname}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
