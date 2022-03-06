import puppeteer from 'puppeteer';
import { timeFormatter } from './timeFormatter.js';

async function CreateEvent(
  clubID,
  clubPassword,
  eventName,
  location,
  startDate,
  endDate
) {
  const {
    startHour,
    startMinute,
    startTimeFrame,
    endHour,
    endMinute,
    endTimeFrame,
  } = timeFormatter(startDate, endDate);
  const browser = await puppeteer.launch();
  try {
    const page = await browser.newPage();
    await page.goto('https://icatcard.ucmerced.edu/');
    await page.click(
      '#block-system-main > div > table > tbody > tr:nth-child(1) > td:nth-child(1) > table > tbody > tr > td:nth-child(2) > div > table > tbody > tr > td:nth-child(2) > div > a'
    );
    await page.waitForSelector('#username');
    await page.type('#username', clubID, { delay: 100 });
    await page.type('#password', clubPassword, { delay: 100 });
    await page.waitForSelector('#fm1 > div.buttons > button');
    await page.click('#fm1 > div.buttons > button');
    await page.waitForNavigation({ waitUntil: 'networkidle0' });
    if (
      page.url() ==
        'https://shib.ucmerced.edu/idp/profile/cas/login?execution=e6s2' ||
      page.url() ==
        'https://shib.ucmerced.edu/idp/profile/cas/login?execution=e6s1'
    ) {
      await browser.close();
      return 'loginFail';
    }

    await page.waitForSelector(
      '#block-system-main > div > table:nth-child(2) > tbody > tr > td:nth-child(4) > form'
    );
    await Promise.all([
      page.click(
        '#block-system-main > div > table:nth-child(2) > tbody > tr > td:nth-child(4) > form'
      ),
      page.waitForNavigation(),
    ]);
    await page.waitForSelector('#event_name');
    await page.type('#event_name', eventName, { delay: 100 });
    await page.type('#event_location', location, { delay: 100 });

    await page.select('#start_hour', startHour);
    await page.select('#start_minute', startMinute);
    await page.select('#start_ampm', startTimeFrame);

    await page.select('#end_hour', endHour);
    await page.select('#end_minute', endMinute);
    await page.select('#end_ampm', endTimeFrame);

    await page.click(
      '#block-system-main > div > form > table > tbody > tr > td:nth-child(2) > div > input'
    );
    return 'success';
  } catch (e) {
    throw e;
  }
}

async function setAttendees(clubID, clubPassword, studentIDs) {
  const browser = await puppeteer.launch();
  try {
    const page = await browser.newPage();
    await page.goto('https://icatcard.ucmerced.edu/');
    await page.click(
      '#block-system-main > div > table > tbody > tr:nth-child(1) > td:nth-child(1) > table > tbody > tr > td:nth-child(2) > div > table > tbody > tr > td:nth-child(2) > div > a'
    );
    await page.waitForSelector('#username');
    await page.type('#username', clubID, { delay: 50 });
    await page.type('#password', clubPassword, { delay: 50 });
    await page.waitForSelector('#fm1 > div.buttons > button');
    await page.click('#fm1 > div.buttons > button');
    await page.waitForNavigation({ waitUntil: 'networkidle0' });
    if (
      page.url() ==
        'https://shib.ucmerced.edu/idp/profile/cas/login?execution=e6s2' ||
      page.url() ==
        'https://shib.ucmerced.edu/idp/profile/cas/login?execution=e6s1'
    ) {
      await browser.close();
      return 'loginFail';
    }

    await page.waitForSelector(
      '#block-system-main > div > table:nth-child(4) > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(7) > form'
    );
    await Promise.all([
      await page.click(
        '#block-system-main > div > table:nth-child(4) > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(7) > form'
      ),
      page.waitForNavigation(),
    ]);
    await page.waitForSelector('#proxid');
    studentIDs.forEach(id => {
      await page.type('#proxid', id, { delay: 50 });
      await page.click('#ucmnetid');
      await page.waitForNavigation();
    });
    return 'success';
  } catch (e) {
    throw e;
  }
}

export { CreateEvent, setAttendees };
