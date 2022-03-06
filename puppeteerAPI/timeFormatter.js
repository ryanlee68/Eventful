function timeFormatter(startDate, endDate) {
  let startHour =
    startDate.getHours() > 12
      ? startDate.getHours() - 12
      : startDate.getHours();
  startHour = startHour.toString();

  let startMinute = startDate.getMinutes() == 0 ? '00' : startDate.getMinutes();
  startMinute = startMinute.toString();

  const startTimeFrame = startDate.getHours() >= 12 ? 'PM' : 'AM';
  console.log(startHour, startMinute, startTimeFrame);
  let endHour =
    endDate.getHours() > 12 ? endDate.getHours() - 12 : endDate.getHours();
  endHour = endHour.toString();
  let endMinute = endDate.getMinutes() == 0 ? '00' : endDate.getMinutes();
  endMinute = endMinute.toString();

  const endTimeFrame = endDate.getHours() >= 12 ? 'PM' : 'AM';
  console.log(endHour, endMinute, endTimeFrame);
  return {
    startHour,
    startMinute,
    startTimeFrame,
    endHour,
    endMinute,
    endTimeFrame,
  };
}

export { timeFormatter, tagRemover };
