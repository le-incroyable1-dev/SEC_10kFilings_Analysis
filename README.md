# SEC 10K Filings Analysis
*Analyzing revenue, profitability, and expense trends from 10-K filings provides critical insights for stakeholders.* These trends offer a snapshot of the company's financial performance and strategic direction over time. Stakeholders can assess growth patterns, operational efficiency, and competitive positioning based on these trends. Additionally, trend analysis informs investment decisions, risk management strategies, and identifies areas for improvement. By understanding the underlying factors driving revenue, profitability, and expense trends, stakeholders can make informed decisions to drive sustainable business growth and mitigate risks.

Sample Information Present in a *Financial Data Section*: 

![image](https://github.com/le-incroyable1-dev/SEC_10kFilings_Analysis/assets/47893192/b6e8a785-40bb-4351-b49f-574f9cc9a4c8)



## Task 1.1: Download Data from the SEC-EDGAR
The *sec-edgar-downloader* (https://sec-edgar-downloader.readthedocs.io/en/latest/) package in Python is used for ease of downloading all the available SEC 10K filings from 1995 to 2023.

## Task 1.2: Text Analysis
The financial data is found by matching "item 8" in an SEC 10K filing. SEC 10K filings have a fairly standard format, which allow most, though sometimes not all filings to be cleaned and analyzed. In some cases, due to how the file formats have evolved over time, the function may match incorrectly, and this has scope of improvement. It matches the starting of the required section and that of the next section, and simply extracts the content required.

Once the correct section is found, it is stripped off all of its HTML code, punctuations and other unnecessary characters (if any) with the help of BeautifulSoup. This section contains several important information about the financial trajectory of the company. These sections are combined and merged from all of SEC 10K filings from all the available years.

In order to analyze the financial data, I use Anthropic Claude LLM Inference API (https://www.anthropic.com/api). This also leaves scope of improvement, where one can possibly use some other API which is more suitable for the current use case. A very specific prompt is submitted to the API which prompts it to generate arrays showing financial trends of revenue, profitability and expense over time. *This requires you to have a valid Anthropic API key, but if that's not possible I use a demo result that I received from a previous prompt.* This result is stripped off to get all the arrays showing the different trends of costs and profits across time through a generic matching process. This also *requires the prompt is good enough to generate the correct format of response majority of the time*.

Once various data over time has been collected, *a line chart is constructed showing the financial trends over time*. These kind of visualizations are especially helpful to investors to understand the company from a broader perspective. With few changes, *this can be modified to generate different insights according to the requirement*.

## Task 2: Construct and Deploy Simple App
Owing to the ease of use, and as it clearly satisfies the current use case, the app is deployed with this code as a backend through streamlit and contains very minimal frontend which can be easily improved. However, for more complex use cases any other tech stack may be used.
(https://sec10kfinancialanalysisapp-moj-kradi.streamlit.app/)
If the streamlit deployment gives unexpected errors, please check these screenshots in the README and let me know of the issue!


Initial View:
![Screenshot 2024-05-11 020005](https://github.com/le-incroyable1-dev/SEC_10kFilings_Analysis/assets/47893192/8eaed424-cdce-4242-8d02-233427491116)


Displaying Demo Visualization:
![Screenshot 2024-05-11 020059](https://github.com/le-incroyable1-dev/SEC_10kFilings_Analysis/assets/47893192/0f87807f-a4b2-43f6-9cb6-0ea3dc48e784)




