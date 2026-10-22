# Software Requirements Specification

*Generated 2026-10-22 14:24 by the requirements-refinement agentic network from `corpus/` (20 source documents).*

## 1. About this document

This document consolidates the software requirements stated across the input corpus. Every requirement has a unique ID, a short name, a paragraph-long explanation, a priority and a list of the source documents it was derived from. Semantically duplicate statements were merged into one requirement; statements discarded as conflicting, nonsensical or out of scope are listed in the Blacklist (section 8).

| Metric | Value |
|---|---|
| Source documents | 20 |
| Candidate statements extracted | 714 |
| Requirements kept | 308 (FR 250, NFR 26, CON 32) |
| Blacklisted | 13 |
| Topics (planner) | 22 in 24 consolidation batches |
| Review rounds | 3 |
| Final review verdict | not approved |
| Models | extractor `gpt-5-mini`, planner `gpt-5.6-luna`, consolidator/reviser `gpt-5.6-luna`, reviewer `gpt-6-luna` |
| Tokens `gpt-5-mini` | 3 calls, 9,337 prompt + 30,381 completion |
| Tokens `gpt-5.6-luna` | 33 calls, 200,436 prompt + 99,789 completion |
| Tokens `gpt-6-luna` | 3 calls, 104,258 prompt + 23,333 completion |

## 2. Identification and priority scale

**IDs.** `FR-nnn` functional requirement, `NFR-nnn` non-functional (quality) requirement, `CON-nnn` constraint, `BL-nnn` blacklisted statement. Source documents are referred to as `Dnn` (section 4).

**Priority (MoSCoW).**

| Priority | Meaning |
|---|---|
| **Must** | Essential for the system to be acceptable. Explicitly demanded by stakeholders, required by a standard or legal obligation, or needed by many libraries for core daily work. The release fails without it. |
| **Should** | Important and clearly wanted by stakeholders, but a temporary workaround exists. Planned for the first release if at all possible. |
| **Could** | Desirable improvement with limited impact, requested by few stakeholders or described as 'nice to have'. Included if time allows. |
| **Won't** | Acknowledged and valid, but explicitly deferred by stakeholders to a later phase. Kept in the document so the need is not lost. |

## 3. Glossary

The following terms are used consistently throughout the requirements.

| Term | Definition | Replaces |
|---|---|---|
| **Audit Log** | An immutable or retained record of administrative, deletion, login, payment, or other auditable actions. | audit trail, audit table, activity log |
| **Bibliographic Record** | The catalog record describing a work or title and its associated volumes and Items. | bib record, bibliographic record, title record |
| **Branch** | A library facility or service point associated with a system or region. | library, location, facility, home library |
| **Canned Report** | A predefined Report with maintained fields, criteria, and execution behavior. | predefined report, standard report, canned query |
| **Circulation** | The set of check-in, checkout, renewal, hold, and related Item-use transactions. | circ, loan activity, circulation activity |
| **Fine** | A monetary charge assessed to a Patron account for a library-related obligation. | bill, charge, debt |
| **Hold** | A Patron request to reserve or retrieve an Item or Bibliographic Record. | request, reservation |
| **Inactivity** | A configurable period since a Patron's last qualifying activity. | inactive period, non-use period |
| **Item** | A physical library copy or material that can be cataloged, circulated, transferred, or deleted. | copy, material, item record |
| **MARC** | The structured machine-readable catalog metadata format used for Bibliographic Records. | MARC field, catalog metadata |
| **Patron** | A person with a library account who uses library services. | borrower, customer, user, member |
| **Query** | A saved or ad hoc set of criteria used to select records or produce a Report. | selection, search, filter expression |
| **Report** | A generated presentation or export of selected library data and metrics. | output, reporting result, statistics report |
| **Report Queue** | The execution queue that tracks, prioritizes, and processes Reports. | job queue, report processing queue |
| **Role** | A named security assignment that grants a defined set of permissions. | user role, access role, security role |
| **Shelf Space** | The physical or estimated capacity occupied by the library collection. | shelf capacity, shelf utilization, shelving space |
| **System** | A library organization or consortium unit containing one or more Branches. | library system, organization, consortium |
| **Template** | A reusable Report definition containing fields, criteria, formatting, and permissions. | report template, report definition |
| **Transaction** | A recorded operational, circulation, financial, or account event. | activity, event, transaction record |
| **Transit** | The movement state of an Item between sending and destination Branches. | in-transit, transfer transit, transit-to, transit-from |

## 4. Source documents

| ID | File | Type | Title / subject | Date |
|---|---|---|---|---|
| D01 | `conversations/conv_pines014_material_volume.eml` | email | Volume reporting - how do we count what we have? | 2009-04-06 |
| D02 | `conversations/conv_pines015_capacity_interface.eml` | email | Can we see all branches at once? | 2009-04-08 |
| D03 | `conversations/conv_pines016_shelf_space.eml` | email | Shelf space vs. usage - help needed | 2009-04-13 |
| D04 | `conversations/conv_pines018_item_transfer.eml` | email | Moving items between branches - utility needed | 2009-05-11 |
| D05 | `conversations/conv_pines019_020_missing_intransit.eml` | email | Missing and damaged items - we need a report | 2009-04-16 |
| D06 | `conversations/conv_pines021_item_purging.eml` | email | Weeding reports - item purging needs | 2009-04-21 |
| D07 | `conversations/conv_pines022_deletions.eml` | email | Tracking deletions - who deleted what? | 2009-04-24 |
| D08 | `conversations/conv_pines023_patron_characteristics.eml` | email | Patron reports by demographics - how? | 2009-04-29 |
| D09 | `conversations/conv_pines024_inactive_patrons.eml` | email | Inactive patrons report needed | 2009-05-05 |
| D10 | `early_draft_srs_galecia.txt` | specification | DRAFT SOFTWARE REQUIREMENTS SPECIFICATION | - |
| D11 | `email_financial_reports.eml` | email | Financial reporting requirements - discussion thread | 2009-07-13 |
| D12 | `email_report_features.eml` | email | Report features and interface requirements | 2009-07-27 |
| D13 | `email_staff_login.eml` | email | Staff login difficulties - need for streamlined access | 2009-04-09 |
| D14 | `evergreen_reference_2009.txt` | reference | EVERGREEN ILS - REPORTING MODULE OVERVIEW | - |
| D15 | `interview_cataloging_2009-05-08.txt` | interview | PINES REPORTS WORKING GROUP - INTERVIEW RECORD | 2009-05-08 |
| D16 | `interview_sysadmin_2009-05-10.txt` | interview | PINES REPORTS WORKING GROUP - INTERVIEW RECORD | 2009-05-10 |
| D17 | `meeting_minutes/meeting_2009-03-15_minutes.txt` | meeting_minutes | PINES REPORTS WORKING GROUP - FIRST MEETING MINUTES | 2009-03-15 |
| D18 | `meeting_minutes/meeting_2009-07-20_minutes.txt` | meeting_minutes | PINES REPORTS WORKING GROUP - SECOND MEETING MINUTES | 2009-07-20 |
| D19 | `meeting_tech_subcommittee_2009-06-30.txt` | meeting_minutes | PINES TECHNICAL SUBCOMMITTEE MEETING NOTES | 2009-06-30 |
| D20 | `survey_results_2009.txt` | survey | PINES STAFF REPORTS SURVEY - RESULTS SUMMARY | - |

## 5. Functional requirements

### 5.1 Authentication Sessions

#### FR-001 - Staff Badge Authentication

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D13, D18

The system shall support staff authentication by either a mapped employee badge followed by the system's required individual authentication step or individual username and password. A badge shall identify exactly one enabled staff account and shall not by itself bypass authentication. Invalid, unassigned, or disabled badges shall not create a session, and acceptance shall verify that both methods identify and record the correct staff account at shared staff terminals.

*Priority rationale:* Secure staff authentication is essential to daily operation, and the sources explicitly require both badge identification and username-and-password access.

#### FR-002 - Staff Login Audit Logging

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D13

The system shall create an Audit Log entry whenever staff login is attempted or completed. Each entry shall identify the staff account, the time, the terminal or access point, and the authentication method, when available. The entries shall support review of which staff member was logged in for security and audit purposes.

*Priority rationale:* Recording staff identity and login context is an explicit audit need and is necessary to establish accountability for authenticated sessions.

#### FR-003 - Unattended Session Protection

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D13

The system shall provide controls that prevent or limit an authenticated staff session from remaining active on an unattended terminal. It shall provide a quick logout action and automatic session expiration after a configurable period of inactivity. When a session expires or is logged out, the terminal shall require staff authentication before protected functions can be used again.

*Priority rationale:* Preventing unattended authenticated terminals is an explicit security need for shared service computers and has no adequate operational workaround.

#### FR-004 - Quick Staff Session Switching

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D13

The system shall allow staff to switch the active authenticated account on a shared service terminal without restarting the application or performing unnecessary terminal setup. The current session shall be ended or protected before another staff member is authenticated. The feature shall support repeated switching among multiple staff members during the day while preserving each account's permissions and audit identity.

*Priority rationale:* Fast switching is clearly needed on shared terminals used by many staff, although a manual logout and login workaround exists.

### 5.2 Bibliographic Reports

#### FR-005 - Bibliographic Fields For Reporting

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D14

The system shall expose Bibliographic Record fields for reporting, including identifier, fingerprint, scan timestamp, record type, edition, language, ISBN, ISSN, UPC, EAN, publisher name, publication date, place of publication, and physical description. These fields shall be selectable or usable as Report criteria and output fields. Acceptance shall verify that each specified field can be retrieved for an applicable Bibliographic Record.

*Priority rationale:* The reporting reference explicitly requires access to these core Bibliographic Record fields.

#### FR-006 - Bibliographic Record Addition Report

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide a Report counting Bibliographic Records added during a selectable period. The Report shall support grouping by the staff member who added each record and by Branch. Acceptance shall verify that additions are attributed to the correct staff member and Branch.

*Priority rationale:* Multiple sources require addition counts by staff member and Branch to support contribution and workload analysis.

#### FR-007 - Bibliographic Record Count Report

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide a Report counting Bibliographic Records in the catalog. The Report shall be retained as a supported bibliographic Canned Report so stakeholders can monitor catalog size. Acceptance shall verify that the reported count matches the selected catalog population.

*Priority rationale:* Counting Bibliographic Records is a core, explicitly requested catalog reporting need and is supported by multiple sources.

#### FR-008 - Bibliographic Record Edit Report

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide a Report counting Bibliographic Records edited during a selectable period. The Report shall support grouping or filtering by the staff member who performed the edit when that information is available. Acceptance shall verify that records edited in the selected period are counted accurately.

*Priority rationale:* Multiple sources explicitly require edit counts to monitor cataloging activity and workload.

#### FR-009 - Bibliographic Records Without Items

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a Report identifying Bibliographic Records with no associated volumes or Items. The Report shall support on-demand and periodic execution so staff can identify incomplete catalog relationships for corrective action. Acceptance shall verify that records without associated volumes or Items are included and records with such associations are excluded.

*Priority rationale:* Several sources explicitly request this quality-control Report to identify incomplete Bibliographic Records.

#### FR-010 - Catalog Data Quality Reports

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D15, D18

The system shall provide data-quality Reports that identify catalog inconsistencies for corrective action. The Reports shall detect Items with invalid Item types, Items with call numbers exceeding the applicable length, and other underlying data problems identified by the data-quality configuration. Acceptance shall verify that each configured condition is detected accurately and that matching records are presented with sufficient identifying data for correction.

*Priority rationale:* Data-quality reporting is explicitly required to support catalog hygiene and corrective action across several concrete conditions.

#### FR-011 - Missing MARC Field Report

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide a Report identifying Bibliographic Records that lack specified MARC fields. The required fields shall be selectable so cataloging staff can check different metadata quality rules. Acceptance shall verify that records missing each selected field are included and records containing the field are excluded.

*Priority rationale:* Multiple sources explicitly require missing-field reporting for catalog quality control and cleanup.

#### FR-012 - Reportable Data Relationships

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D14

The system shall support reporting across key relationships between Bibliographic Records and Items, Items and Circulation actions, Patrons and Circulation actions, Patrons and money records, and staff actors and Circulation actions. These relationships shall permit related data to be joined without losing the source-record association. Acceptance shall verify representative cross-record Reports using each required relationship.

*Priority rationale:* Cross-record relationships are essential for producing meaningful bibliographic and operational Reports from the reporting data model.

#### FR-013 - Reportable Record Types

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D14

The system shall support reporting on Bibliographic Records, Items, Patrons, Circulation actions, Holds actions, money records, and staff actor records. Each listed record type shall be available as a reportable data source. Acceptance shall verify that a Report or Query can select records from every required type.

*Priority rationale:* The reporting reference explicitly identifies these core record types as necessary coverage for the reporting system.

#### FR-014 - Circulation Canned Reports

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D14

The system shall retain and support the specified Circulation Canned Reports for checkout counts, renewal counts, non-cataloged activity, and Circulation counts by shelving location. Each Canned Report shall remain executable with its maintained fields and criteria. Acceptance shall verify that all listed Canned Reports are available and produce the expected measures.

*Priority rationale:* The reference explicitly identifies these existing Canned Reports as supported reporting capabilities, although they are secondary to Bibliographic Record reporting in this topic.

#### FR-015 - Monthly Patron Addition Report

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a Report showing the number of Patrons added for each month. The Report shall support a selectable reporting period so registration trends can be examined over time. Acceptance shall verify that each Patron is counted in the correct month based on the addition date.

*Priority rationale:* The report is explicitly requested but concerns a narrower analytical need than core Bibliographic Record reporting.

#### FR-016 - Patron Canned Reports

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D14

The system shall retain and support Canned Reports for total Patron counts and Patron counts by Branch. The Branch grouping shall use the Patron's associated home Branch. Acceptance shall verify both Report types and confirm that grouped counts reconcile with the total count.

*Priority rationale:* The reference explicitly requests these maintained Patron Reports, but they are less central to Bibliographic Reports than catalog data quality and count Reports.

### 5.3 Circulation Analytics

#### FR-017 - Checkin Count Report

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a Checkin Count Report showing the number of check-ins for the selected reporting period and scope. The Report shall use check-in transactions rather than renewal transactions. Acceptance shall verify that the resulting count matches the included check-in records.

*Priority rationale:* A dedicated check-in count is a core Circulation Report explicitly listed in the requirements.

#### FR-018 - Checkin Method Counts

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D20

The system shall count check-ins individually and cumulatively by method, including book-drop, terminal, and self-service check-ins. Reports shall allow staff to distinguish each method and view the combined check-in total. Acceptance shall verify both method-specific and cumulative counts.

*Priority rationale:* Method-level check-in analysis is explicitly requested in both the specification and staff survey.

#### FR-019 - Checkout Count Report

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a Checkout Count Report that counts checkout transactions only. The Report shall exclude check-ins, Holds, and other transaction types from the checkout total. Acceptance shall verify the count against checkout records for the selected criteria.

*Priority rationale:* A checkout-only count is a core Circulation Report explicitly required by the specification.

#### FR-020 - Checkout Type Counts

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D20

The system shall count checkout transactions individually and cumulatively by type, including staff checkout, self-checkout, staff renewal, self-checkout renewal, online renewal, and OPAC renewal. Reports shall distinguish each type and provide a combined total. Acceptance shall verify that all listed types can be selected and counted separately.

*Priority rationale:* Detailed checkout and renewal type counts are explicitly required by both the specification and staff survey.

#### FR-021 - Circulation Counts By Type

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide total Circulation counts with separate counts for categorized, non-categorized, checkout, renewal, and non-cataloged transactions where applicable. The total shall combine category and non-category Circulation data without double-counting transactions. Reports shall display the component counts and the resulting total.

*Priority rationale:* Accurate total Circulation and its transaction-type breakdown are fundamental to circulation-volume reporting.

#### FR-022 - Core Circulation Activity Metrics

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12

The system shall provide activity Reports containing checkouts, check-ins, Holds placed, and Holds filled. These metrics shall show Circulation traffic and volume of use for activity and board reporting. Each metric shall be independently identifiable and countable in the generated Report.

*Priority rationale:* The same four metrics are explicitly required across the specification, email, and survey and are central to Circulation analytics.

#### FR-023 - Distinct Checkin Timestamp

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D14, D20

The system shall record and expose a check-in date and time that represents a physical check-in and does not include renewal events. Reports shall be able to filter and count transactions using this check-in timestamp. Acceptance shall verify that renewals do not alter check-in timestamp results.

*Priority rationale:* Separating check-ins from renewals is necessary for accurate check-in analytics and is explicitly confirmed by multiple sources.

#### FR-024 - Multi Scope Transaction Aggregates

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D20

The system shall generate transaction Reports for Holds placed, Holds filled, and checkouts at Patron, Branch, selected Branch-group, System, and county scopes. Reports shall provide counts for each requested scope and support Patron-level results where applicable. Hold results shall be subtotaled by Hold type, including active, frozen, and frozen-until Holds.

*Priority rationale:* Multi-level aggregation is explicitly required for operational and geographic Circulation analysis.

#### FR-025 - Overdue Item Reports

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall produce Reports listing Items overdue by a configurable number of days, including Items more than the specified threshold and Items marked longoverdue by the System. Reports shall support daily operations, shelf reading, and Patron follow-up, and shall include available Patron contact information for recovery actions. The system shall also provide a list of long-overdue Items without requiring a separate workflow.

*Priority rationale:* Overdue reporting is repeatedly requested for daily operations, shelf reading, and Patron contact.

#### FR-026 - Renewals Count Report

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a Renewals Count Report showing the number of renewal transactions for selected reporting criteria. Renewal counts shall be distinguishable from checkout and check-in counts. Acceptance shall verify the result against renewal transaction records.

*Priority rationale:* Renewals are a core Circulation transaction and are explicitly required as a dedicated count.

#### FR-027 - Circulation By Patron County

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide Circulation counts by circulation Branch or location further broken down by Patron county. Reports shall show the count for each county within each selected circulation location. Acceptance shall verify that the breakdown reflects the Patron county associated with each qualifying transaction.

*Priority rationale:* Geographic usage analysis is explicitly requested in multiple sources but is less essential than core Circulation metrics.

#### FR-028 - Circulation By Patron Home Branch

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide Circulation counts by circulation location broken down by the Patron's home Branch. Reports shall show counts for each home Branch within each selected circulation location. Acceptance shall verify that the grouping uses the Patron home Branch stored for the transaction's Patron.

*Priority rationale:* Home-Branch comparison is explicitly required for analyzing where Patrons circulate Items, though it is a specialized dimension.

#### FR-029 - Circulation Counts By Dewey

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide Reports counting Circulation by Dewey classification. Staff shall be able to analyze usage for individual classifications or selected Dewey classification ranges. Acceptance shall verify that counts are grouped according to the Items' Dewey values.

*Priority rationale:* Dewey-based usage analysis is explicitly requested but is a specialized analytical dimension.

#### FR-030 - Circulation Counts By MARC

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide Circulation Reports grouped or filtered by MARC fields associated with the relevant Bibliographic Record or Item. Staff shall be able to associate usage counts with selected catalog metadata. Acceptance shall verify that a selected MARC field or value produces the corresponding Circulation counts.

*Priority rationale:* MARC-based usage analysis is explicitly requested for metadata-related analysis but is not a core transaction function.

#### FR-031 - Circulation Counts By Shelf Location

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide Circulation counts grouped by shelving location. Reports shall identify the shelving location associated with the circulated Item and show its corresponding count. Acceptance shall verify counts for selected shelving locations and reporting criteria.

*Priority rationale:* Shelving-location usage supports collection and service analysis but is not required for basic transaction totals.

#### FR-032 - Circulation Modifier Category Counts

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide Circulation counts grouped by circulation modifier and category fields such as Cat1 and Cat2. Reports shall support values including Adult, YA, and Juv when those values exist in the data. Acceptance shall verify counts for each selected modifier and category combination.

*Priority rationale:* Modifier and category analysis is explicitly requested, but it is more specialized than core transaction totals.

#### FR-033 - Claims Returned Report

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide a Claims Returned Report listing Items associated with Patron claims that the Items were returned. The Report shall support selection of qualifying claims and display the associated Item information. Acceptance shall verify that claimed-return Items appear and unrelated Items do not.

*Priority rationale:* A Claims Returned Report is explicitly requested for circulation follow-up and appears in both the specification and reference material.

#### FR-034 - Date-Based Item Use Counts

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide total use counts for Items and usage counts broken down by selected date ranges. Supported ranges shall include fiscal-year and monthly periods. Acceptance shall verify that the total and each date-range count reflect qualifying use transactions within the specified dates.

*Priority rationale:* Time-based use analysis is explicitly requested and supports routine circulation trend reporting.

#### FR-035 - Hold Placement Methods

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D20

The system shall count Holds and report how each Hold was placed, including at a staff desk, at a public computer inside a Branch, or remotely. Reports shall support both method-specific counts and identification of the placement method for each qualifying Hold. Acceptance shall verify that Holds placed through each listed method are correctly classified.

*Priority rationale:* Hold placement analysis is explicitly requested in both the specification and staff survey, but is less central than basic Circulation totals.

#### FR-036 - Include Uncataloged Circulation

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D15

The system shall count Transactions involving uncataloged Items and include them in overall Circulation statistics and Reports. The resulting totals shall reflect usage alongside Transactions involving cataloged Items. Reports shall also identify the portion attributable to uncataloged Items so staff can analyze that activity without completed Bibliographic Records.

*Priority rationale:* Complete Circulation reporting requires uncataloged Transactions, although manual reconciliation can temporarily compensate for its absence.

#### FR-037 - Item Use Count Filtering

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide Reports listing Items whose total use count meets a specified threshold or matches a specified total use count. Staff shall be able to use the resulting list for Circulation analysis. Acceptance shall verify correct inclusion and exclusion of Items at, above, and below the selected count criteria.

*Priority rationale:* Use-count filtering is explicitly requested in the specification and reference material for circulation analysis.

#### FR-038 - Last Circulation Date

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D14

The system shall provide a separate last circulation date field for each applicable Item. Reports shall use this field to identify the most recent Circulation independently from other dates. Acceptance shall verify that the field records and displays the latest qualifying circulation date.

*Priority rationale:* A separate last-circulation value is explicitly requested to support accurate use and circulation reporting.

#### FR-039 - Transaction Dimension Grouping

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D20

The system shall allow transaction Reports and Queries to group results by hour, terminal, Branch, and System. Reporting shall support all transactions or a selected transaction type, including check-ins, checkouts, fines collected, and Patron registrations where those transaction records are available. Acceptance shall verify that each dimension produces separate counts and that transaction-type selection limits the results correctly.

*Priority rationale:* Dimension-based transaction analysis is explicitly requested by the survey and specification for workload and trend analysis.

#### FR-040 - Items By Fines Stopped Reason

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide a Report listing Items associated with a selected fines-stopped reason. Staff shall be able to review the associated Item and reason information for circulation follow-up and auditing. Acceptance shall verify that only Items with the selected reason are included.

*Priority rationale:* The report is explicitly requested but supports a specialized fine-handling workflow rather than core circulation analytics.

### 5.4 Collection Capacity

#### FR-041 - All Branch Capacity Overview

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D02, D10, D18

The system shall provide a high-level Report or dashboard showing capacity and inventory metrics for all Branches in a System. The view shall aggregate centralized capacity data across Branches and present the Branches together for at-a-glance resource allocation and collection planning. Acceptance shall verify that a user can view all Branches in one system-wide overview and that the displayed aggregate values match the centralized source data.

*Priority rationale:* Multiple sources identify system-wide capacity visibility as essential for daily monitoring and resource allocation.

#### FR-042 - Break Down Collection Categories

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D01, D03

The system shall break down collection volume by cataloged genre and format classifications, such as adult fiction and board books. Reports shall support grouping and aggregation by these category fields. The category values shall be taken from the existing catalog metadata used for the collection.

*Priority rationale:* Category composition is explicitly required to understand and manage collection capacity by genre and format.

#### FR-043 - Cross-Branch Capacity Access

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D02

The system shall allow Branch managers and other authorized Roles to view capacity information for Branches beyond their home Branch. Access shall be governed by the applicable Role permissions rather than by an unconditional restriction to the manager's home Branch. Unauthorized Roles shall not gain access through this capability.

*Priority rationale:* Cross-Branch visibility is explicitly required for allocation decisions and must be controlled to remain appropriate for each Role.

#### FR-044 - Define Capacity Metrics

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D02

The system shall define and identify the capacity metrics used in Reports, such as Item counts, Shelf Space, configured limits, or other agreed measures. Each displayed metric shall have a precise meaning and distinguish physical collection volume from operational capacity where applicable. Users shall be able to determine which metric is represented in an overview or Report.

*Priority rationale:* Unambiguous capacity definitions are essential for interpreting all capacity Reports and avoiding inconsistent decisions.

#### FR-045 - Drill Into Branch Capacity

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D01, D02

The system shall allow users to select a Branch from a capacity overview and view its detailed capacity information. Branch detail shall select Items using the Branch or Item location associated with that Branch. The detail view shall provide the supporting metrics needed to understand the selected Branch's collection volume.

*Priority rationale:* Branch-level detail is necessary for staff to act on the system-wide capacity information.

#### FR-046 - Estimate Shelf Space

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D03

The system shall estimate Shelf Space when direct Shelf Space data is unavailable. It shall use available Item dimensions when present and an Item-count proxy when dimensions are missing, while allowing authorized administrators to configure or tune the fallback estimation method. Reports shall identify or consistently apply the selected estimation basis and make the resulting values available for capacity analysis.

*Priority rationale:* Shelf Space analysis cannot be implemented reliably because the source data does not directly track Shelf Space.

#### FR-047 - Material Volume Report

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D01, D10, D15

The system shall generate a Material Volume Report for a selected Branch or System as of a specified point in time. The Report shall provide category and total counts, including new acquisitions, Items currently on the shelf, and Items currently checked out, with checked-out Items included in the total. Users shall be able to apply the relevant acquisition time selection, and results shall be reproducible for governance, board reporting, collection management, and quarterly assessment.

*Priority rationale:* A dated volume Report with collection breakdowns is explicitly identified as a key governance and collection-management requirement.

#### FR-048 - Shelf Space Comparison Report

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D03, D10, D15, D18

The system shall provide a Shelf Space Report that compares, for each selected genre and format, the percentage of total Circulation, the percentage of the collection, and the percentage of total Shelf Space. The Report shall calculate collection percentages from Item counts and Circulation percentages from checkout totals for the selected scope and date range. It shall support Branch-level and System-level results so staff can compare local and aggregated collection allocation. The presentation shall support identifying mismatches between space and use.

*Priority rationale:* This comparison is requested repeatedly by the working group and directly supports collection allocation and physical shelving decisions.

#### FR-049 - Branch Comparison View

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D03

The system shall provide a comparison view that displays the capacity or collection breakdown for multiple Branches side by side. The view shall use a multi-column or matrix presentation that enables users to compare Branch results and identify outliers. The compared metrics shall correspond to the selected Report and scope.

*Priority rationale:* Side-by-side comparison is an important analysis aid for spotting differences between Branches, with a workable alternative of reviewing Branches separately.

#### FR-050 - Capacity Trend Reporting

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D02

The system shall provide Reports or views showing changes in Branch capacity over time. Results shall support historical comparison or time-series analysis so staff can determine whether capacity is growing or shrinking. The selected time range and comparison points shall be identifiable in the output.

*Priority rationale:* Trend analysis is explicitly requested for long-term planning, although current capacity reporting can operate without it.

#### FR-051 - Collection Volume Trend Reporting

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D01

The system shall provide Reports or views showing changes in collection volume over time. Staff shall be able to use historical comparisons or time series to analyze changes in collection size. The output shall identify the time periods represented so that volume changes can be verified.

*Priority rationale:* Historical collection-size analysis is requested for trend planning but is not required to produce a current volume count.

#### FR-052 - Compare Branch Capacity

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D03, D18

The system shall provide Reports that compare capacity and collection metrics across multiple Branches. A selected Branch shall be comparable with the System average for the same genre or format where those dimensions are reported. The comparison shall support analysis of local collection conditions against peer and system-wide results.

*Priority rationale:* Branch-to-system and cross-Branch comparison is a clear management need, but Branch detail alone provides a temporary alternative.

#### FR-053 - Configurable Aggregation Levels

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D03, D09

The system shall allow Reports to aggregate and present collection and capacity results at configurable organisational levels. Supported levels shall include at least Branch and System, and the configuration shall accommodate additional levels such as Home Library or County when those dimensions exist in the data. The selected grouping shall be reflected in the Report results.

*Priority rationale:* Multiple sources require results at different organisational levels, while a fixed set of levels provides a temporary workaround.

#### FR-054 - Consolidated Volume Report

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D01

The system shall provide a single consolidated Report that combines the volume counts needed from the multiple existing screens used by staff. The Report shall eliminate the need to collect and reconcile those counts manually across separate interfaces. Its output shall be available as one coherent result for the selected reporting scope.

*Priority rationale:* The request addresses a significant recurring manual effort, but existing screens provide a temporary workaround.

#### FR-055 - Export Capacity Data

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D02, D03

The system shall allow users to export selected or filtered capacity data to common spreadsheet formats, including CSV. The export shall contain the capacity values represented by the selected view or Report. Users shall be able to use the exported data for spreadsheet analysis and director-level Reports.

*Priority rationale:* Multiple stakeholders need spreadsheet-based analysis, although viewing capacity within the system provides a temporary alternative.

#### FR-056 - Filter Acquisition Date Ranges

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D01

The system shall allow users to filter new acquisitions by a date range. It shall provide common presets such as the last 30, 60, and 90 days. The resulting Report shall show the volume acquired within the selected range.

*Priority rationale:* Standard acquisition windows are specifically requested and provide useful recurring capacity insight, although custom calculations remain possible without presets.

#### FR-057 - Filter Branch Capacity

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D02

The system shall allow users to filter Branch capacity results by available Branch attributes, including region, Branch type, and current load. Filtering shall limit the overview or Report to Branches matching the selected values. The resulting subset shall retain its capacity metrics.

*Priority rationale:* Stakeholders explicitly requested attribute-based filtering to focus capacity analysis on relevant Branch subsets.

#### FR-058 - Filter Reports By Date

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D03

The system shall allow users to filter applicable collection and Shelf Space Reports by arbitrary date ranges, such as months, quarters, or other start and end dates. Users shall be able to compare results for different periods, including seasonal or quarterly comparisons. The selected date range shall be visible or otherwise identifiable in the Report.

*Priority rationale:* Quarterly and period-based analysis is explicitly needed for capacity review, though current snapshots remain a usable fallback.

#### FR-059 - Group Branch Capacity

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D02

The system shall allow users to group Branch capacity results by System, region, or another configured logical grouping. Grouped results shall present aggregated capacity values for each group. The grouping shall reduce the need to inspect individual Branches when analyzing larger collections.

*Priority rationale:* Grouping is an important usability improvement for reviewing capacity across many Branches, but individual Branch results remain a workaround.

#### FR-060 - Report Holds By Category

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D01

The system shall report the number of Holds for a selected Branch or System. It shall also break Hold counts down by the same collection categories used for volume analysis where category data is available. The Report shall present Hold pressure alongside Item counts so staff can compare demand with collection composition.

*Priority rationale:* Hold pressure by category supports collection capacity decisions, but a temporary overall Hold count can provide limited insight.

#### FR-061 - Show Historical Volume

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D01

The system shall allow users to request collection volume as of a specified historical date rather than only the current snapshot. The calculation shall use available acquisition and Item status data to represent the volume at that point in time. The selected as-of date shall be identifiable in the resulting Report.

*Priority rationale:* Historical snapshots are explicitly requested for analysis, although current volume reporting is the essential baseline.

#### FR-062 - Sortable Capacity Results

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D02

The system shall allow users to sort the Branch capacity list or table by available fields such as Branch name, capacity metric, or load. Sorting shall update the displayed results without changing the underlying data. The available sort fields shall be identifiable in the interface.

*Priority rationale:* Sorting is explicitly requested to support routine analysis, although users can temporarily review an unsorted list.

#### FR-063 - Color-Coded Capacity Indicators

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D02

The system shall display capacity status indicators using distinguishable colors for under-capacity, approaching-full, and at-or-over-capacity states. The interface shall use green for under capacity, yellow for getting full, and red for at or over capacity, or provide an equivalent accessible status indication. The status shall be derived from the configured capacity thresholds.

*Priority rationale:* Color coding improves rapid interpretation but is a desirable presentation enhancement rather than a prerequisite for capacity reporting.

#### FR-064 - Customizable Volume Categories

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D01

The system shall allow authorized staff to define and customize the categories and category groupings used in a volume breakdown. The selected categories shall be applied consistently when generating the relevant Material Volume Report. This shall allow different Branches or Systems to use their preferred classification sets.

*Priority rationale:* Custom classification supports differing library practices but is requested by fewer sources and is not necessary for basic volume reporting.

#### FR-065 - List Checked-Out Items

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall produce a list of Items currently checked out for the selected Branch or applicable collection scope. The list shall identify the checked-out Items that contribute to the reported collection volume. Users shall be able to use the list to inspect the checked-out component of capacity.

*Priority rationale:* An Item-level checked-out list is useful for investigation, but aggregate checked-out counts satisfy the core capacity need.

### 5.5 Deletion Auditing

#### FR-066 - Aggregate Deletion Counts

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D07, D10

The system shall produce deletion counts aggregated by Branch and by System. Reports shall support filtering or aggregation by date range, person or process responsible for the deletion, and record type. Users shall be able to obtain total deletion counts for configurable periods such as a month, quarter, or year. The reporting capability shall include the number of deleted Items.

*Priority rationale:* Multiple sources require location-level, system-wide, period-based, and record-type deletion counts for routine oversight.

#### FR-067 - Capture Deletion Audit Events

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D07, D10, D15, D20

The system shall record deletion events for Items, Patrons, Bibliographic Records, and other deleted record types. Each event shall identify the record type, record identifier, person or process that performed the deletion, deletion timestamp, and Branch or other location context. Where available, the event shall also capture the pre-deletion status and the deletion reason. These records shall allow staff to investigate accidental deletions and establish who deleted what, when, and where.

*Priority rationale:* Deletion traceability is explicitly required by multiple sources and is essential for auditing and accountability.

#### FR-068 - Query Deleted Record Audit

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D07

The system shall provide a Report interface for viewing, filtering, and retrieving deletion audit events. Staff shall be able to list deleted records by record type and period, including all records of a selected type deleted during a specified quarter or other date range. The resulting audit evidence shall provide authoritative records and counts that can be used to demonstrate compliance with retention schedules.

*Priority rationale:* Audit and compliance users need direct access to detailed deletion evidence, and this need is explicitly identified as important.

#### FR-069 - Filter Transaction Audit Reports

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide audit Reports for deletion-related transactions filtered by exact date and time, workstation, or staff member. Users shall be able to apply each criterion individually and in combination where corresponding audit data exists. The results shall support detailed auditing and troubleshooting of the selected transactions.

*Priority rationale:* Detailed transaction filtering improves audit investigations but is less central than capturing and retaining deletion events.

#### FR-070 - Log Denied Deletion Attempts

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D07

The system shall record deletion attempts that are denied because of authorization failures or other system controls. Each denied attempt shall identify the attempted record when available, the actor, timestamp, location, and denial outcome. Administrators shall be able to use these records to detect repeated or inappropriate deletion attempts.

*Priority rationale:* Denied-attempt auditing supports security monitoring and is explicitly requested, but the system can operate with a temporary monitoring workaround.

#### FR-071 - Rank Deleting Staff

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D07

The system shall provide a Report that ranks staff or other deletion actors by the number of deletion events attributed to them. The ranking shall be based on a selectable reporting period and the captured deletion audit events. Administrators shall be able to use the result to identify unusually high deletion activity for investigation.

*Priority rationale:* Ranking deletion actors is a useful monitoring enhancement requested by one source but is not essential to basic deletion auditing.

### 5.6 Documentation Accessibility

#### FR-072 - Integrated Searchable Help

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14, D16, D18, D19

The system shall provide an online HTML help system integrated with the reporting interface. The help system shall be hierarchical, cross-linked, searchable, easy to navigate, and include context-sensitive guidance where appropriate. It shall describe and illustrate system functions so staff can obtain documentation without leaving the relevant interface or contacting IT for routine assistance.

*Priority rationale:* Multiple sources explicitly require integrated online help, including high-priority requests for comprehensive assistance during routine reporting work.

#### FR-073 - Administrative Error Feedback

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D18, D19

The system shall provide meaningful high-level error reports and feedback through the front-end interface. For report or Query failures, it shall provide Local and Global System Administrators with low-level, Query-specific diagnostic details, including the affected table, field, and type of error when available. The feedback shall enable administrators to diagnose and correct failures without relying solely on developers.

*Priority rationale:* Detailed error feedback is requested by multiple sources and materially improves administration, although manual developer diagnosis provides a temporary workaround.

### 5.7 Financial Reporting

#### FR-074 - Associate Financial Transactions

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D11

The system shall associate Fines, charges, waivers, and e-commerce Transactions with the relevant Patron and Item records. These associations shall be available for account review, reporting, reconciliation, and audit. A financial Transaction shall remain identifiable through the records to which it applies.

*Priority rationale:* Associating financial events with Patron and Item records is necessary for accurate balances, reporting, and reconciliation.

#### FR-075 - Core Financial Reports

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide and maintain financial Reports for Bills Currently Owed by Patrons, Detailed Payments Received, and Aged Debt. The payments Report shall show transaction-level detail for reconciliation, and the Aged Debt Report shall show overdue balances using aging buckets with sufficient detail for collection activity. The Reports shall remain available as supported financial reporting functions.

*Priority rationale:* These financial Reports are explicitly identified as established core outputs for billing, reconciliation, and collections.

#### FR-076 - Maintain Payment Ledger

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D11

The system shall maintain a detailed ledger of Patron payments. Each payment shall identify the specific Fine or charge to which it was applied, allowing staff to trace payment activity for reconciliation and audit. The ledger shall retain transaction-level details needed to explain account balances.

*Priority rationale:* The working-group requirement marks payment traceability as critical to reconciliation and auditing.

#### FR-077 - Query High-Balance Accounts

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D11

The system shall allow authorized staff to query and list Patron accounts whose balance exceeds a specified dollar threshold. The threshold shall be supplied by staff or configured as an operational value. The query and user interface shall allow staff to find qualifying accounts promptly, avoiding a slow manual process, and shall identify accounts requiring collection or account-management attention.

*Priority rationale:* Identifying accounts over a balance threshold is an explicit operational need for collection activity, and prompt access is needed to replace the current slow manual process.

#### FR-078 - Report Fines By Period

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D11

The system shall provide Reports of Fines and charges accrued during a selectable time period. Staff shall be able to group or filter results by charge type, including overdue, damaged Item, and lost Item charges. Supported periods shall include configurable date ranges and common periods such as the previous twelve months, year to date, and the previous month.

*Priority rationale:* Fines and charge reporting is a core financial reporting need explicitly requested by multiple sources.

#### FR-079 - Report Patron Account Balances

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D11

The system shall provide Reports of Patron account balances at individual Patron, Branch, and System levels. Staff shall be able to determine the balance associated with each Patron and aggregate balances for a Branch or the entire System. The Report shall identify the reporting scope used for each result.

*Priority rationale:* Balance reporting is a core financial-account function requested by multiple sources.

#### FR-080 - Report Payments By Method

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D11

The system shall provide Reports of payments received during a selectable time period. Results shall be broken down by payment method or channel, including cash, credit card, check, staff desk, self-check station, and OPAC where recorded, and shall support Branch-level reporting. These breakdowns shall support daily, monthly, and end-of-month reconciliation.

*Priority rationale:* Payment reporting by time, method, and Branch is important for routine reconciliation and is explicitly marked important by stakeholders.

#### FR-081 - Track Financial Transactions

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D17

The system shall record and provide verification of financial Transactions related to library operations. Staff shall be able to use the recorded transactions to support accounting, reconciliation, and auditing. The system shall preserve sufficient transaction details to verify each financial event.

*Priority rationale:* Accurate transaction tracking is essential to all financial reporting, reconciliation, and audit activities.

#### FR-082 - Join Financial Data Sources

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D11

The system shall allow financial Queries and Reports to combine data associated with Patron records and Item records. Staff shall be able to use relationships between the two data sources to produce cross-referenced financial results. The combined results shall preserve the identifying context of both the Patron and Item.

*Priority rationale:* Cross-referencing Patron and Item financial data enables important reports that cannot be produced from either source alone.

#### FR-083 - Provide Director Financial Reporting

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D18

The system shall provide financial Reports suitable for director-level review. Directors shall be able to review financial summaries and supporting details within their authorized scope. The Reports shall cover relevant account, Fine, payment, waiver, and balance information without requiring manual compilation.

*Priority rationale:* Director-level financial review is an explicit stakeholder need, but it can initially rely on the underlying operational Reports.

#### FR-084 - Report Historical Bill Snapshots

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D14, D20

The system shall provide a historical snapshot Report for Patron bills. Authorized staff shall be able to review the state of bills at selected points in the past. The snapshots shall support audit, dispute investigation, and historical financial reporting.

*Priority rationale:* Historical bill states support auditing and dispute resolution and are requested by multiple sources, though they are not required for every daily transaction.

#### FR-085 - Report Item Monetary Values

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D11, D14

The system shall generate Reports of Item monetary values using the purchase price or equivalent value stored in Item records. Staff shall be able to report on the entire collection or a selectable subset filtered by attributes such as status, format, collection, call number, or shelving location. The system shall query and aggregate the values to produce totals and summaries.

*Priority rationale:* Item valuation supports collection financial analysis and is requested in several sources, but it is less central than account and payment processing.

#### FR-086 - Report Voided Transactions

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a Report of voided financial Transactions. Each result shall include sufficient transaction detail to support audit and financial control review. Authorized staff shall be able to identify when and what financial activity was voided.

*Priority rationale:* Voided-transaction reporting supports financial control and auditability, although it is narrower than routine payment reporting.

#### FR-087 - Report Waived Fines

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D11

The system shall track and report Fines waived during a selectable time period. Staff shall be able to view waiver results by Branch so that each Branch can monitor its waiver activity and budget. The Report shall identify the applicable period and Branch for each aggregate.

*Priority rationale:* Branch-level waiver reporting supports budget control and is explicitly requested by several financial sources.

#### FR-088 - Report Alternative Payments

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a detailed Report of alternative payment and adjustment types, including forgive, work, and goods payments. The Report shall identify each relevant Transaction and its amount or adjustment. Staff shall be able to use the results to track these nonstandard payment types.

*Priority rationale:* Alternative payment reporting is useful for specialized reconciliation but is requested by only one source.

### 5.8 Hold Management

#### FR-089 - Stale Holds Report

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide a Report identifying Holds that have remained on the Hold shelf awaiting Patron pickup beyond a configured acceptable period. The Report shall identify the Holds requiring cleanup or staff intervention. Staff shall be able to use the Report to support purging or follow-up actions.

*Priority rationale:* Two sources request this capability and stale Holds require timely operational action to keep fulfillment processes accurate.

#### FR-090 - Unfilled Holds Report

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall produce a Report identifying Holds that remain unfilled. The Report shall provide the information needed by acquisitions and operational staff to investigate unmet Patron demand and fulfillment backlogs. Staff shall be able to use the Report for follow-up and demand planning.

*Priority rationale:* Two sources explicitly request this report and unfilled Holds directly affect Patron service and acquisition decisions.

#### FR-091 - Annual Holds Placed Count

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide an annual count of Holds placed. The count shall be calculated for a specified year and shall be available in a Report. Staff shall be able to use the result for Hold trend analysis and planning.

*Priority rationale:* Annual Hold volume is an explicitly requested planning metric, but manual aggregation of transaction data provides a temporary workaround.

#### FR-092 - Bibliographic Records With Holds

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall generate a periodic Report listing Bibliographic Records with one or more active Holds. The Report shall identify the affected Bibliographic Records and the associated Hold presence so staff can monitor demand. The Report shall support recurring or on-demand execution according to the system's reporting capabilities.

*Priority rationale:* This is a clearly requested operational report that supports monitoring demand, although staff have temporary alternatives through existing Hold searches.

#### FR-093 - Holds Purchase Alert

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide a Report identifying demand-driven opportunities to purchase additional copies or titles based on Holds. The Report shall identify Holds or demand patterns that indicate existing supply may be insufficient. Acquisitions staff shall be able to use the Report to evaluate potential purchases.

*Priority rationale:* Two source documents request this capability because it supports purchasing decisions, but purchasing can continue temporarily through manual demand review.

#### FR-094 - IntraPINES Loan Reporting

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide Reports of IntraPINES loans across Systems and Branches. Users shall be able to view the loans at overall, System-grouped, and Branch-grouped levels. The Reports shall support monitoring inter-System and inter-Branch lending activity and related metrics.

*Priority rationale:* Multiple candidates request these reporting scopes, indicating broad stakeholder interest, although lending activity can temporarily be monitored through lower-level transaction data.

#### FR-095 - Item-Level Holds Report

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a periodic Report of Holds placed on specific Items. The Report shall distinguish Item-level Holds from Holds placed only at the Bibliographic Record level. Staff shall be able to use the Report to monitor and manage Item-specific fulfillment activity.

*Priority rationale:* Item-level Hold visibility is an explicitly requested operational need that supports fulfillment, though some manual Hold review may be possible as a workaround.

#### FR-096 - Items Received For Holds

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a Report listing Items received to satisfy Holds. The Report shall identify the received Items and their associated Hold fulfillment activity. Staff shall be able to use the Report to reconcile receipt and completion of Hold fulfillment.

*Priority rationale:* This operational reconciliation report is explicitly requested and supports fulfillment tracking, although staff may temporarily reconcile receipts manually.

#### FR-097 - Items Sent For Holds

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a Report listing Items sent to fulfill Holds. The Report shall support identification of the sending Branch and the relevant destination or supplier activity when that information is available. Staff shall be able to use the Report to track Hold-related Item movement and reconcile fulfillment.

*Priority rationale:* Tracking Items sent for Holds is explicitly requested and supports fulfillment reconciliation, but staff can temporarily use transaction or Transit records.

#### FR-098 - Items Without Recent Checkouts

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall generate a periodic Report listing Items that have not been checked out during a configurable number of days. Staff shall be able to specify the value of X days used to identify qualifying Items. The Report shall present the resulting Items for collection review or operational follow-up.

*Priority rationale:* This report supports collection and operational decisions and is explicitly requested, but staff can temporarily identify such Items through other circulation analysis.

#### FR-099 - Missing Items Report

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a periodic Report of Items marked or otherwise recorded as missing. The Report shall identify the affected Items and their relevant catalog or Branch information when available. Staff shall be able to use the Report for investigation and operational follow-up.

*Priority rationale:* Periodic visibility of missing Items is explicitly requested and supports operations, but staff may temporarily obtain the information through Item-status searches.

### 5.9 Item And Catalog Reports

#### FR-100 - Item Activity Reports

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide separate Reports for Items added, Items edited, total Item counts, and lists of Items added within a selectable date range. Each Report shall present the applicable count or Item list using the selected reporting period and available identifying fields. Acceptance shall verify count accuracy, date-range inclusion for added Items, and correct identification of edited Items.

*Priority rationale:* Multiple sources explicitly request Item counts and cataloging activity Reports for operational monitoring.

#### FR-101 - Periodic Last Item Report

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14, D15

The system shall provide a periodic Report identifying each Bibliographic Record whose title has exactly one remaining Item in the System. The Report shall support recurring execution and include sufficient identifying metadata and holdings information for catalogers to avoid accidental deletion and update external catalog records. Acceptance shall verify that titles with exactly one remaining Item are included and titles with multiple Items are excluded.

*Priority rationale:* The working-group sources identify last-Item reporting as critical for preventing accidental deletion and supporting catalog maintenance.

#### FR-102 - Standard Item Canned Reports

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D14

The system shall maintain Canned Reports for Items added, Items deleted, Items currently checked out, Items overdue by a specified number of days, and Items with missing status. Each Canned Report shall retain its supported fields and execution behavior for staff use. Acceptance shall verify that all listed Canned Reports are available and return records matching their defined conditions.

*Priority rationale:* The maintained standard Item Reports are explicitly identified as required operational reporting capabilities.

#### FR-103 - Weeding Reports With Use History

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14, D18, D20

The system shall provide weeding Reports that help staff identify Items for retention or withdrawal decisions. Each applicable result shall include the date of last Circulation and the number of Circulations for the Item. Acceptance shall verify that staff can use the Report to review Items and that both use-history fields are populated accurately.

*Priority rationale:* The sources describe weeding Reports as frequently used and specifically require last-Circulation information for collection decisions.

#### FR-104 - Collection Age By Location

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide a Report of collection age metrics grouped by call number or shelving location. Staff shall be able to use the results to assess the age of different collection segments. Acceptance shall verify that age values are calculated from Item or collection dates and are grouped under the requested call-number or shelving-location dimension.

*Priority rationale:* Two sources request collection-age analysis to support collection management and assessment.

#### FR-105 - Configurable Weeding Criteria

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D15

The system shall allow staff to identify Items for weeding using configurable criteria. Criteria shall support conditions such as Missing status for more than a specified number of months and an explicit discard or weed status. Acceptance shall verify that staff can configure the criteria and that the resulting Report includes only Items satisfying them.

*Priority rationale:* Configurable criteria are explicitly requested to support different local collection-management practices.

#### FR-106 - Item Last Edit Date

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D14, D15

The system shall provide an Item last-edit-date field in Reports that represents the most recent metadata edit. Circulation Transactions shall not update or be treated as Item edits for this field. Acceptance shall verify that editing an Item changes the field while a subsequent Circulation Transaction does not.

*Priority rationale:* Two sources require a reliable distinction between catalog editing and Circulation activity for report interpretation.

#### FR-107 - Items By Bibliographic Content

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a Report listing Items whose associated Bibliographic Record contains a specified string or field value. Staff shall be able to specify the content to match, such as a designated marker in the record. Acceptance shall verify that matching Items are returned and nonmatching Bibliographic Records are excluded.

*Priority rationale:* Content-based Item selection supports catalog quality work but is less central than standard status and date reports.

#### FR-108 - Items By Creation Date

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide Reports listing Items created within a specified creation-date range. Staff shall be able to enter or select the start and end dates for monitoring acquisitions and processing. Acceptance shall verify that Items inside the inclusive range are returned and Items outside it are excluded.

*Priority rationale:* Two sources request this report for acquisitions and processing monitoring, indicating a recurring operational need.

#### FR-109 - Low Use Weeding Report

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a weeding Report listing Items whose total use count is below a specified threshold. Staff shall be able to provide or select the threshold used for the Report. Acceptance shall verify that Items below the threshold are included and Items at or above it are excluded.

*Priority rationale:* Low-use identification is a direct and practical basis for collection weeding decisions.

#### FR-110 - Missing Item Report

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a Report listing Items whose status is Missing. The Report shall identify each matching Item and its relevant catalog or Branch information. Acceptance shall verify that Items with Missing status are included and Items with other statuses are excluded.

*Priority rationale:* Identifying Missing Items is a common collection-control need, although detailed missing-pattern analysis is separate.

#### FR-111 - Periodic Invalid Item Reports

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a periodic Report identifying Items whose Item type is invalid. The Report shall identify each matching Item sufficiently for staff to locate and correct the data. Acceptance shall verify that invalid Item types are included, valid Item types are excluded, and the Report can execute on its configured periodic schedule.

*Priority rationale:* This targeted catalog-quality Report supports correction work but is less central than core circulation and Item reporting.

#### FR-112 - Invalid Patron Home Branch Report

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a periodic Report identifying Patrons whose home Branch value is invalid. The Report shall identify the affected Patron account and the invalid value for correction. Acceptance shall verify that invalid home-Branch references are included and valid references are excluded.

*Priority rationale:* This is a useful data-quality report but is outside the core Item and catalog reporting workload.

#### FR-113 - Missing Patterns By Shelf

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D15

The system shall provide Reports that aggregate missing or damaged Items by shelf or shelving location over time. Staff shall be able to examine recurring patterns, such as repeated losses from the same shelf, to inform collection-placement decisions. Acceptance shall verify aggregation by the selected shelf dimension and across a specified time period.

*Priority rationale:* Pattern analysis can improve collection decisions but is a specialized enhancement beyond basic Missing Item reporting.

#### FR-114 - Periodic Long Call Number Reports

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a periodic Report identifying Items whose call number exceeds the configured or supported length. The Report shall show the affected Item and its call number for catalog review. Acceptance shall verify that Items above the applicable length are included, shorter call numbers are excluded, and the Report executes on its configured periodic schedule.

*Priority rationale:* Long call-number detection is useful for catalog maintenance but has limited impact compared with core Item and collection Reports.

### 5.10 Item Transfers

#### FR-115 - Batch Item Transfer Utility

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04, D10, D15

The system shall provide a utility for authorized staff to transfer batches of Items between Branches, mobile units, outreach collections, and temporary locations. The utility shall support bulk relocation as part of collection balancing and scheduled programs. Acceptance shall include transferring a selected batch while recording its source and destination.

*Priority rationale:* Batch transfer is the core purpose of this topic and is explicitly requested by multiple sources as a crucial operational capability.

#### FR-116 - Manually Select Transfer Items

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04, D10, D15, D20

The system shall allow staff to manually select individual Items or titles from transfer-query results. Selection shall support choosing a subset of results rather than requiring the entire result set to be transferred. Acceptance shall include selecting and deselecting individual results before a transfer is initiated.

*Priority rationale:* Staff explicitly require targeted selection to prevent unsuitable Items from being included in bulk actions.

#### FR-117 - Protect Checked-Out Items

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04

The system shall prevent event-based automatic reversion when a transferred Item has been checked out at the destination Branch. The Item shall remain at the destination until the checkout-related condition no longer prevents reversion or an authorized staff member resolves it. Acceptance shall include confirming that a checked-out Item is not automatically returned by an otherwise matching reversion rule.

*Priority rationale:* Preventing reversion of an Item in active use is a direct safety requirement that avoids disrupting Patron Circulation.

#### FR-118 - Query Transfer Candidates

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04, D10, D15, D20

The system shall allow authorized staff to query Items to identify candidates for transfer using criteria such as Branch, section, genre, circulation history, and inactivity. Staff shall be able to run the query and use its results as the input to a transfer operation. Acceptance shall include identifying Items such as those in a specified section that have not circulated for a configured period.

*Priority rationale:* Candidate identification is required for practical batch transfers and is requested across several sources.

#### FR-119 - Restrict Transfer Permissions

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04

The system shall restrict transfer operations to staff whose Role grants the required transfer permissions. Unauthorized staff shall be prevented from initiating or applying Branch transfers. Acceptance shall include allowing an authorized Role to perform a transfer and denying the same action to an unauthorized Role.

*Priority rationale:* Transfer permissions affect Item custody and location integrity, so access control is essential.

#### FR-120 - Time-Based Item Reversion

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04, D10, D15

The system shall automatically revert transferred Items to their original location after a configured period. Staff shall be able to configure the applicable reversion period for a transfer or transfer group. Acceptance shall include reverting an eligible Item after the configured period and preserving the original location as the destination.

*Priority rationale:* Automatic return after temporary deployments is explicitly described as important and is needed to manage recurring mobile and outreach transfers.

#### FR-121 - Update Item Locations

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04, D10, D15, D20

The system shall update the location of selected Items in bulk to reflect movement to a new Branch or temporary location. The update shall change the relevant Item records as part of the transfer workflow. Acceptance shall include verifying that every selected Item has the new location and that unselected Items are unchanged.

*Priority rationale:* Updating Item locations is the essential system action that records a completed transfer and is requested by multiple sources.

#### FR-122 - Criteria-Based Item Reversion

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04

The system shall support automatic reversion rules triggered by configurable Item criteria or status events. Rules shall support events such as an Item becoming sold or returned and shall remove or revert the Item from the applicable transfer placement as configured. Acceptance shall include configuring a supported event and verifying the resulting reversion for an eligible Item.

*Priority rationale:* Event-based reversion is requested in several forms and reduces errors when temporary transfer conditions change.

#### FR-123 - Generate Transfer Pull Lists

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04, D10

The system shall generate printable pull lists for the Items selected for transfer. Each pull list shall identify the Items needed for physical retrieval and the relevant transfer source and destination information. Acceptance shall include producing a readable list containing all and only the Items in the transfer selection.

*Priority rationale:* Pull lists directly support the physical retrieval step and are explicitly identified as a transfer mechanism, although manual lists provide a temporary workaround.

#### FR-124 - Manage Temporary Locations

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04

The system shall allow authorized staff to create and use temporary locations for events, outreach programs, mobile units, and temporary warehouses. Items shall be assignable to these locations through the transfer workflow and shall retain their original location for later reversion. Acceptance shall include assigning Items to a temporary location and making that location available for the configured transfer process.

*Priority rationale:* Temporary placement is explicitly needed for events and outreach operations, though permanent Branch transfers remain the core use case.

#### FR-125 - Preview And Confirm Transfers

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04

The system shall display a preview of pending transfer actions before applying them. The preview shall include at least the Item count and source and destination locations, and the system shall require explicit staff confirmation before changing records. Acceptance shall include canceling from the preview without changes and confirming to apply the displayed transfer.

*Priority rationale:* Confirmation reduces costly bulk-transfer errors and is clearly requested, while a carefully reviewed manual process is a temporary workaround.

#### FR-126 - Print Transit Labels

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04

The system shall generate printable Transit labels for Items included in a transfer. Labels shall support barcode-based identification during physical movement and shall be associated with the relevant Items. Acceptance shall include printing labels for a selected transfer and verifying that each label identifies its Item.

*Priority rationale:* Labels improve reliable physical handling and tracking of transferred Items, but transfers can temporarily proceed with manual labeling.

#### FR-127 - Schedule Reversion Processing

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04

The system shall run a scheduled background task that evaluates transferred Items against configured time-based and event-based reversion rules. The task shall apply eligible reversion actions without requiring staff to inspect every transfer manually. Acceptance shall include scheduling an evaluation and verifying that eligible Items are processed while ineligible Items remain unchanged.

*Priority rationale:* Scheduled processing is necessary for dependable automatic reversion, although staff could temporarily perform the checks manually.

#### FR-128 - Track Item Transfer History

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04

The system shall maintain a history of transfers for each Item. The history shall include transfer dates, locations, and enough information to determine how often the Item has been transferred during a specified period. Acceptance shall include viewing an Item history and counting its transfers within a selected time range.

*Priority rationale:* Transfer history supports identification of problematic movement patterns and is explicitly requested for operational analysis.

#### FR-129 - Undo Transfer Operations

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04, D20

The system shall allow an authorized staff member to undo a transfer operation and restore affected Items to their previous locations. The undo action shall identify the transfer being reversed and shall not alter unrelated Item locations. Acceptance shall include undoing a completed transfer and verifying restoration of all affected Items.

*Priority rationale:* Undo capability provides important recovery from bulk-action errors, although authorized staff could otherwise restore locations manually.

#### FR-130 - Alert On Transfer Issues

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04

The system shall notify designated staff when a transfer is delayed or encounters a configured transfer issue. Notifications shall identify the affected transfer and provide enough information for staff to investigate and take corrective action. Acceptance shall include generating a notification for a simulated delay or issue and verifying delivery to the designated recipients.

*Priority rationale:* Issue alerts improve operational response but are a desirable enhancement because staff can monitor transfers through other procedures.

### 5.11 Management Analytics

#### FR-131 - Branch Capacity Analysis

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D17

The system shall provide Reports and analysis of Branch capacity and the distribution of the collection among Branches. The analysis shall support evaluation of available capacity and identification of an optimal collection distribution. Managers shall be able to use the results to support collection planning across Branches.

*Priority rationale:* Branch capacity and collection distribution are explicitly requested in multiple documents and support system-level planning.

#### FR-132 - Collection Use Analysis

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D17

The system shall provide Reports and analysis of the collection and its use by Patrons to support collection management decisions. The analysis shall support metrics such as Circulation statistics and collection utilization. The resulting Reports shall enable management to evaluate use patterns and make evidence-based collection decisions.

*Priority rationale:* Collection-use analysis is explicitly requested in multiple documents and directly supports core collection management decisions.

#### FR-133 - Manager Planning Reports

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide Reports that library managers can use for planning and evaluation. The Reports shall present relevant operational or program metrics in a form suitable for comparing results against management objectives. The system shall make the Reports available for routine management review.

*Priority rationale:* Managerial planning and evaluation are explicitly identified as a general reporting need for routine library management.

#### FR-134 - Staff Productivity Analysis

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D17, D20

The system shall provide Reports and analysis of staff productivity and workflow for operational management and process improvement. The analysis shall support productivity metrics, including time spent per Transaction where that data is available. Managers shall be able to use the results to inform staffing and workflow decisions.

*Priority rationale:* Staff productivity analysis is requested in three candidates and supports operational management, staffing, and process improvement.

#### FR-135 - Collection Development Reports

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D20

The system shall support Reports for collection development activities. The Reports shall provide relevant collection development metrics through either maintained Canned Reports or easily created custom Reports. The available metrics shall support evaluation and planning of collection development decisions.

*Priority rationale:* Collection development reporting is a clearly stated stakeholder need, although it can initially be supported through general Report capabilities.

#### FR-136 - Executive Strategic Reports

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall produce aggregated, high-level Reports for Library Administrators. The Reports shall support strategic planning and preparation of board presentations. Aggregation shall summarize relevant data and metrics at a level appropriate for executive and board review.

*Priority rationale:* Executive and board reporting is explicitly requested, but operational management reports provide a temporary workaround for some planning needs.

#### FR-137 - Program Attendance Reports

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D20

The system shall support Reports for recording and analyzing attendance at library programs. The Reports shall allow attendance data to be summarized for program evaluation and planning. The results shall support management review of program participation.

*Priority rationale:* Program attendance reporting is explicitly requested and supports evaluation and planning, but it is less central than broad management analytics.

### 5.12 Patron Demographics

#### FR-138 - Geographic Age Demographics

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D20

The system shall produce aggregated demographic statistics from transaction data grouped by geographic region, including ZIP code, and Patron age range. The outputs shall support programming, outreach, collection, and service planning. Acceptance shall verify that users can obtain counts or statistics for selected geographic and age groupings.

*Priority rationale:* Geographic and age analysis is requested by several sources and is a core demographic reporting need.

#### FR-139 - Geographic Patron Counts

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide Patron counts grouped by county, city, and ZIP code. The Report shall support both a county-only view and combined geographic groupings for analysis of Patron distribution and outreach planning. Acceptance shall verify that counts reflect each populated geographic value and that missing values are handled consistently.

*Priority rationale:* Multiple sources explicitly request county, city, and ZIP-level Patron counts for geographic analysis and outreach.

#### FR-140 - Patron Characteristic Reporting

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D08, D10

The system shall allow Queries and Reports to filter and group Patron records by age or birthdate, postal code, county, home Branch, Patron type, and preferred language. These characteristics shall be sourced authoritatively from the Patron data source and shall support both individual filters, such as a specific postal code, and grouped analysis. Acceptance shall verify that each supported characteristic can be selected, filtered, and grouped while remaining correctly associated with its Patron record.

*Priority rationale:* The requested demographic Reports depend on consistent Patron characteristics and are explicitly identified as essential planning capabilities.

#### FR-141 - Patron Demographic Planning

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D17, D18

The system shall provide Reports and analysis of Patron demographics and interests to support service planning, programming, outreach, and collection development. The analysis shall use available Patron characteristics and support community-level interpretation without requiring individual Patron identification. Acceptance shall include generation of demographic outputs suitable for planning decisions.

*Priority rationale:* Multiple stakeholder sources identify demographic analysis as a core purpose of this reporting capability.

#### FR-142 - Reportable Patron Fields

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D14

The system shall expose the defined Patron fields for use in Report generation, including identifier, barcode, OPAC status, home Branch, Patron type, email, address lines, city, state, ZIP code, birth date, and creation date. Field exposure shall follow the applicable privacy and permission rules. Acceptance shall verify that each supported field can be selected or used by an authorized Report.

*Priority rationale:* These fields provide the data foundation required for demographic grouping and filtering.

#### FR-143 - Total Patron Count

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a Report containing the total number of Patrons in the System. The count shall be available for demographic and operational tracking. Acceptance shall verify that the result can be reconciled with the selected Patron population.

*Priority rationale:* A total Patron count is a basic operational measure needed for demographic reporting and planning.

#### FR-144 - Circulation By Patron Age

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide Patron counts and Circulation counts grouped by defined Patron age demographic buckets. Users shall be able to compare the Patron population and Circulation activity across age groups. Acceptance shall verify that each included Patron and Circulation Transaction is assigned to the correct configured age bucket or handled according to the defined missing-age rule.

*Priority rationale:* Age-based population and Circulation analysis is explicitly requested but is not required for basic Circulation reporting.

#### FR-145 - Filter By Survey Name

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D19

The system shall allow users to select a survey by its human-readable name when defining a Report filter. The system shall resolve the selected name to the corresponding survey identifier internally. Acceptance shall verify that filtering by survey name produces the same records as filtering by its identifier.

*Priority rationale:* Multiple sources request this usability improvement because it avoids requiring users to know internal survey identifiers.

#### FR-146 - List Barred Patrons

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide a Report listing Patrons with barred status. Authorized staff shall be able to use the list to manage access and enforcement actions. Acceptance shall verify that the Report includes all Patrons matching the selected barred status and excludes others.

*Priority rationale:* The capability supports operational Patron administration, although it is not required for core demographic analysis.

#### FR-147 - New Patron Demographic Counts

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall Report Patrons added during the previous month grouped by demographic category. The Report shall identify the reporting month and provide counts for each available demographic category. Acceptance shall verify that the result includes only Patrons added during the specified previous month.

*Priority rationale:* New Patron trends support planning and outreach, but a manual count can temporarily provide this information.

#### FR-148 - Patron Behavior Analytics

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D20

The system shall produce statistics and analytical outputs that support understanding and prediction of Patron behavior and Item use. Outputs shall support measures such as renewal likelihood, return speed, average return time, and the percentage of renewals. Acceptance shall verify that these measures can be generated from available historical data.

*Priority rationale:* Behavior prediction is explicitly requested but is less central than basic demographic reporting and can have temporary manual workarounds.

#### FR-149 - Patron Count By Branch

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide counts of Patrons grouped by their home Branch. The Report shall support Branch-level metrics, allocation, and service planning. Acceptance shall verify that each count is based on the Patron home Branch value.

*Priority rationale:* Branch-level Patron distribution is useful for allocation and planning, although it is less fundamental than overall demographic counts.

#### FR-150 - Patron Count By Profile

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide Patron counts grouped by profile group or Patron type. The Report shall support segmentation and targeted service planning. Acceptance shall verify that each Patron is counted in the configured profile group associated with the reporting population.

*Priority rationale:* Profile-based segmentation is a clearly requested demographic capability with practical planning value.

#### FR-151 - Patron Lists By Expiration

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall produce lists of Patrons grouped or filtered by card or account expiration date. The lists shall support renewal management and outreach. Acceptance shall verify that Patrons appear in the correct expiration-date grouping or match the selected expiration-date criteria.

*Priority rationale:* Expiration-date lists support routine Patron management and outreach but are not essential to demographic analysis.

#### FR-152 - Patron Reports By Survey Answer

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide counts of Patrons grouped by selected survey answer and lists of Patrons who selected a specified answer. The count and list functions shall use the selected survey and its recorded answers, with access controlled according to applicable Patron-data permissions. Acceptance shall verify that grouped counts are accurate and that every listed Patron has the selected answer.

*Priority rationale:* Survey-based analysis and follow-up are explicitly requested and support targeted service planning.

#### FR-153 - Staff Password Audit Report

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide a Report of staff accounts that includes the date of the last password change and the account expiration date when available. The Report shall support security auditing and compliance review. Acceptance shall verify that authorized staff can obtain these fields for each included staff account.

*Priority rationale:* Security auditing is important, but this specialized Report can be supplemented temporarily by administrative account review.

#### FR-154 - Patron Lists By Note Text

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall produce lists of Patrons whose notes contain specified wording. Authorized users shall be able to provide the wording used for matching and use the result for compliance or case management. Acceptance shall verify that the list contains only Patrons whose searchable notes match the specified wording.

*Priority rationale:* Note-based Patron retrieval is useful for specialized case management but is requested by only one source.

#### FR-155 - Voter Registration Counts

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall Report voter registration survey response counts aggregated by week. The Report shall support monitoring of voter registration campaign activity. Acceptance shall verify that each weekly count includes only responses recorded for the selected voter registration survey.

*Priority rationale:* Weekly voter registration monitoring is a specialized use case requested by one source and is not essential to general demographic reporting.

#### FR-156 - Voter Responses By County Week

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall Report voter survey responses aggregated by county and week. The Report shall support civic engagement outreach and analysis without exposing individual response records in the aggregate. Acceptance shall verify that responses are assigned to the correct county and reporting week.

*Priority rationale:* This is a specialized survey analysis requested by the working materials but has limited impact on general Patron demographics.

### 5.13 Patron Inactivity

#### FR-157 - Configurable Inactivity Thresholds

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D09

The system shall allow staff to define the Inactivity threshold as any whole number of days. The system shall provide common presets for approximately monthly, quarterly, semi-annual, and annual periods, including 30, 90, 180, and 365 days. Staff shall be able to select a preset or enter a different value for each Report execution.

*Priority rationale:* The inactive Patron definition varies by operational use, and several candidates explicitly require both adjustable and preset periods.

#### FR-158 - Inactive Patron Exclusions

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D09

The system shall allow staff to exclude selected Patron types, flags, or categories from the inactive Patron Report. Exclusion criteria shall support cases such as do-not-disturb Patrons, VIPs, staff Patrons, and Patrons who have opted out of communications. Excluded records shall not appear in the resulting inactive Patron list.

*Priority rationale:* Excluding protected or unsuitable accounts is necessary to avoid inappropriate cleanup or outreach.

#### FR-159 - Inactive Patron Report

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D08, D09, D10, D14

The system shall generate a Report listing Patrons with no qualifying Circulation or electronic activity within a configurable Inactivity period. The Report shall support filtering by System, home Branch, county, and other available Patron criteria, including compound demographic and activity conditions. Staff shall be able to use the Report for account maintenance, cleanup, outreach, and reactivation efforts. The Report shall be available for manual execution.

*Priority rationale:* Multiple sources identify the inactive Patron list as an essential operational need for cleanup and outreach.

#### FR-160 - Aggregated Patron Metrics

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D08

The system shall provide aggregate metrics for Patron Reports, including Patron counts and applicable Circulation or checkout counts. Staff shall be able to group these metrics by Patron characteristics such as age range or home Branch. The Report shall present the aggregated values for the selected filters and groups.

*Priority rationale:* Aggregated metrics extend the inactive-Patron analysis and are explicitly requested for planning and comparison.

#### FR-161 - Branch Cleanup Assignment

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D09

The system shall allow authorized staff to view inactive Patron results in the context of a home Branch and assign cleanup or follow-up work to a specific Branch. An assignment shall identify the relevant Branch and associated inactive Patron list or selection. Staff shall be able to use the assignment to coordinate operational follow-up.

*Priority rationale:* Branch assignment supports the stated cleanup workflow but is less fundamental than generating the inactive Patron list.

#### FR-162 - Configurable Age Brackets

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D08

The system shall allow staff to define custom age brackets for Patron filtering and grouping within a Report. Brackets may use locally selected ranges such as 0-5, 6-10, and 11-15 or other nonoverlapping ranges. The selected bracket definitions shall be applied consistently to the Report results.

*Priority rationale:* Multiple candidates request configurable age groupings to support different reporting and planning needs.

#### FR-163 - Inactive Patron Mailing Addresses

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D09

The system shall include each inactive Patron's current mailing address in the inactive Patron Report when that address is available. The address fields shall be associated with the corresponding Patron record. Staff shall be able to use the Report output to perform direct outreach such as postcard mailings.

*Priority rationale:* Mailing addresses directly support the requested outreach use case but are not required to identify inactivity.

#### FR-164 - Inactive Patrons By Branch

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D09

The system shall provide counts of inactive Patrons grouped by Branch when the Report is viewed at the System level. Staff shall be able to compare Branch counts to identify locations with the greatest number of inactive accounts. The counts shall reflect the selected Inactivity threshold and other active filters.

*Priority rationale:* Branch-level counts support System administration and are explicitly requested for identifying cleanup priorities.

#### FR-165 - Incomplete Patron Data Handling

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D08

The system shall handle missing values in optional Patron fields without failing or silently excluding the affected Patron records. Reports shall retain those records and represent unavailable field values as null or an equivalent explicit empty value. The behavior shall be consistent for filtering, grouping, and output.

*Priority rationale:* Incomplete Patron data is expected in normal operations, and predictable handling is necessary to prevent misleading results.

#### FR-166 - Logical Filter Combination

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D08

The system shall allow staff to combine Report filters with logical AND and OR operators. The resulting Query shall apply the combined conditions to the selected Patron records. The system shall make it possible to express compound criteria without requiring separate Reports for each condition.

*Priority rationale:* Compound filtering is needed for practical Patron targeting, but a limited single-condition workaround exists.

#### FR-167 - Outstanding Fine Flag

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D09

The system shall identify inactive Patrons who have outstanding Fines in the inactive Patron Report. The Report shall provide a flag or separate indicator that distinguishes those accounts from inactive Patrons without outstanding Fines. Staff shall be able to use this indicator when deciding on cleanup or outreach actions.

*Priority rationale:* Outstanding Fines affect how staff handle inactive accounts and are explicitly requested as a separate operational distinction.

#### FR-168 - Scheduled Inactivity Reports

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D09

The system shall allow authorized staff to schedule recurring executions of the inactive Patron Report, including periodic runs such as quarterly cleanup checks. The system shall also support manual ad hoc execution. Each execution shall use the configured Inactivity threshold and Report criteria for that run.

*Priority rationale:* Recurring inactive-Patron checks are part of the stated cleanup process, while manual execution remains an available workaround.

### 5.14 Platform Integration

#### FR-169 - Centralized Multi-Branch Operations

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D18, D19

The system shall support centralized management processes that accept input from and provide services to multiple Branches within a System or consortium. It shall maintain a centralized operational view while supporting services across the participating locations. Acceptance shall verify that authorized central processes can receive and serve data for multiple Branches.

*Priority rationale:* Centralized operation across multiple Branches is fundamental to the target consortium architecture.

#### FR-170 - Protect Deleted Item Visibility

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall prevent front-line staff from modifying Report Templates in ways that expose deleted Items when such visibility is not permitted. Template permissions or validation shall enforce the applicable restriction. Acceptance shall verify that a front-line staff account cannot create or alter a Template to display deleted Items.

*Priority rationale:* Preventing inappropriate exposure of deleted Items is an explicit control on staff reporting capabilities.

#### FR-171 - Query OPAC Activity Data

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D18, D19

The system shall interact with the OPAC to query patron-created data needed for Reports, including Holds and Circulation transactions. The system shall use this data to reflect patron activity in management Reports. The integration shall be read-only and shall not create, alter, or delete OPAC data.

*Priority rationale:* Reports require reliable access to patron activity while preserving the OPAC as the system of record for public-facing data.

#### FR-172 - WorldCat Integration Support

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D15

The system shall provide integration with, or direct assistance for accessing, WorldCat records. Catalogers shall be able to examine or edit relevant WorldCat records when handling last-copy Items. The integration shall help prevent accidental deletion of Items that may require cataloging review.

*Priority rationale:* The working group explicitly identified WorldCat integration as critical for protecting last-copy Items.

#### FR-173 - Historical Data Reporting

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D20

The system shall allow authorized users to request a Report showing the state of relevant data as of a specified past date. The Report shall preserve historical values for attributes that may have changed since that date, such as shelving location. Acceptance shall verify that a historical request returns values associated with the selected date rather than only current values.

*Priority rationale:* Historical views are clearly requested but are less central to daily platform operation than core integrations and performance.

#### FR-174 - Historical Reporting Warehouse

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14, D19

The system shall support historical reporting through a reporting warehouse or equivalent historical data store. Authorized users shall be able to retrieve data for a specified date or date range to perform point-in-time analysis without relying solely on current operational values. Acceptance shall verify that historical snapshots can be queried for requested periods without adversely affecting production operations.

*Priority rationale:* Historical analysis is repeatedly requested and valuable, but current-data reporting provides a temporary operational alternative.

#### FR-175 - Integrate Vendor Data

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D18, D19

The system shall interface with vendor websites through published APIs or automated transfer of standard-format data files. Supported integrations shall accommodate formats such as USMARC21 and EDIFACT. Where provided by a vendor, the system shall handle EDI ordering data.

*Priority rationale:* Vendor integration is important for operational data exchange, but a temporary manual exchange process may be possible.

#### FR-176 - Local Administrative Configuration

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D17

The system shall allow Local System Administrators to configure settings and reporting options for their organizational units. It shall restrict each administrator's configuration scope to the applicable Branch or organizational unit. Acceptance shall verify that authorized local administrators can change local settings and run system Reports without requiring central administration.

*Priority rationale:* Local configuration is clearly requested by multiple stakeholders, but central administration provides a temporary workaround.

#### FR-177 - Migrate Environment Configuration

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D19

The system shall support migration of configuration between development, testing, and production environments. Authorized staff shall be able to export and import Report Templates, permission settings, and saved Queries. Acceptance shall verify that exported configuration can be imported into another supported environment without re-creating each element manually.

*Priority rationale:* Environment migration reduces deployment risk and is explicitly required by the later technical-subcommittee decision.

#### FR-178 - Reports For Notices Sent

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide Reports on notices sent to Patrons. The Reports shall distinguish at least pre-overdue, overdue, and Hold notices. Authorized staff shall be able to use the results to track Patron communications.

*Priority rationale:* Notice tracking is a concrete operational reporting need, although it is narrower than the platform's core integration capabilities.

### 5.15 Record Purging

#### FR-179 - Batch Item Status Conversion

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D06, D10, D15

The system shall provide a Report and tools to select Items for batch conversion from one status to another. Staff shall be able to review the Items selected for conversion and apply the new status to many Items in one operation, such as changing Items from missing to discard/weed. The operation shall support large selections efficiently to reduce manual cataloging and cleanup work.

*Priority rationale:* Batch status conversion is repeatedly requested as a core efficiency need for large-scale cleanup.

#### FR-180 - Controlled Purge Execution

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D06

The system shall present purge candidates in a read-only view before any destructive operation is performed. It shall require a distinct confirmation step before deleting or purging selected records and shall provide safeguards such as review and permission checks to prevent accidental mass deletion. The safeguards shall apply to both individually selected records and large batch selections.

*Priority rationale:* Separate review and confirmation are essential to prevent irreversible loss of collection data.

#### FR-181 - Identify Purge Candidates

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D06, D10

The system shall provide a utility and Reports that identify Item records eligible for purging using staff-configurable criteria. Criteria shall include specific Item status values, time spent in a status, last Circulation date or elapsed time since last Circulation, and combinations of criteria using logical operators such as AND and OR. The resulting candidate list shall support planning and review of weeding and cleanup actions.

*Priority rationale:* Identifying records safely and consistently is the core purpose of Record Purging and is requested by multiple sources.

#### FR-182 - Purge Volumes And Orphans

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D06, D10, D15

The system shall provide a cleanup function that can delete a volume together with its associated Items when the operation is authorized. It shall identify and remove Bibliographic Records with no associated Items and other orphaned records, including records whose parent relationship is missing. The cleanup function shall support bulk processing and shall provide an appropriate removal or repair action for each detected orphan type.

*Priority rationale:* Removing empty volumes and orphaned catalog records is a core data-cleanup need requested by multiple sources.

#### FR-183 - Sole Item Purge Flagging

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D06

The system shall determine whether each Item considered for purge is the only Item for its Bibliographic Record within a selected Branch or across the System. Purge candidate Reports shall clearly flag the applicable sole-Item condition and identify relevant holdings or ownership information. The information shall help staff review local and System-wide consequences before deletion and update external catalog records when necessary.

*Priority rationale:* Avoiding deletion of local or System-wide sole Items is a critical collection-protection requirement.

#### FR-184 - Report Deleted Sole Copies

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide Reports of Items that were deleted and were the last copy within the System or a Branch. The Reports shall identify the deleted Item and the scope in which it was the sole copy. Staff shall be able to use the results for local collection maintenance and for updating external catalog records such as WorldCat.

*Priority rationale:* Post-deletion sole-copy reporting is clearly requested for catalog maintenance, although it is less central than preventing inappropriate deletion.

#### FR-185 - Schedule Purge Operations

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D06

The system shall allow authorized administrators to run purge-identification Reports and cleanup utilities either manually or according to a configurable schedule. Schedules shall support recurring executions, including an annual execution such as at the end of each year. The system shall execute the configured operation without requiring staff to start it manually at the scheduled time.

*Priority rationale:* Recurring automated purging is important for ongoing weeding but manual execution provides a workable interim approach.

### 5.16 Report Authoring

#### FR-186 - Boolean Query Logic

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D14

The system shall allow staff to combine Query criteria with Boolean operators including AND, OR, and NOT. The Query interface shall support nested Boolean logic for compound selection criteria. The resulting Query shall apply the specified logic consistently when selecting records for a Report.

*Priority rationale:* Complex Boolean logic is required to express many practical reporting selections and is explicitly demanded across sources.

#### FR-187 - Controlled Template Editing

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12

The system shall allow administrators to specify, for each Template and applicable Role, which filters and display fields staff may alter. The system shall preserve protected criteria and fields when a Template is modified, such as preventing staff from exposing deleted Items while allowing an authorized call number range. Changes to Template parameters shall not compromise the correctness, integrity, or certified consistency of the resulting Report.

*Priority rationale:* Controlled editing is necessary to preserve dependable results while still allowing authorized staff customization.

#### FR-188 - Display Query Criteria

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D14

The system shall display the Query selections and criteria used to generate a Report alongside or within its results. The displayed criteria shall identify the filters and selections that produced the result set. This shall enable staff to understand and verify how the Report was produced.

*Priority rationale:* Showing criteria is important for interpreting and verifying Reports and is explicitly requested by several sources.

#### FR-189 - Field Selection And Filtering

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D14, D20

The system shall expose the relevant available database fields for Report authoring, including Item fields such as identifier, barcode, label, copy number, Branch, status, circulation modifier, call number, purchase date, purchase price, and shelving location. Staff shall be able to select fields for a Query through the authoring interface, including visual drag-and-drop selection where supported. Reports and Queries shall allow filtering by selected standard, advanced, and custom fields, and shall support basic result sorting.

*Priority rationale:* Selecting and filtering report fields is a core capability needed for targeted daily reporting.

#### FR-190 - Interactive Report Authoring

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D14, D17, D20

The system shall provide a browser-based report writer that enables staff, including front-line and supervisory staff, to create, store, and execute custom Reports. The interface shall support report authoring without developer assistance and shall retain locally created Reports for later reuse. Staff shall be able to contribute report content needed by their Branch or System.

*Priority rationale:* Interactive staff authoring is central to creating the custom Reports required by multiple stakeholders.

#### FR-191 - Report Template Management

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D14, D17, D18

The system shall allow administrators to create, maintain, version, and distribute reusable Templates for staff across the System. Templates shall contain standardized Report definitions that can be reused by multiple Branches without recreating the underlying criteria and fields. The system shall support the set of Templates needed for standardized reporting across the participating Branches.

*Priority rationale:* Reusable standardized Templates are a core requirement requested by administrators and the working group for consistent System-wide reporting.

#### FR-192 - Run Or Modify Templates

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D20

The system shall allow staff to run an authorized Template without changing its definition. It shall also allow staff to create an authorized modified version for individual reporting needs while preserving the original Template. Administrator-defined limits and edit controls shall be applied whenever a staff member modifies a Template.

*Priority rationale:* Running standardized Templates and making controlled local variations are explicitly required for routine staff reporting.

#### FR-193 - Support Specified Report Definitions

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall support the Report definitions and fine-grained reporting requirements specified in Appendix A and Appendix B of the applicable requirements specification. Each specified definition shall be representable through the system's available fields, criteria, and output behavior. Conformance shall be verified against the approved Appendix A and Appendix B examples.

*Priority rationale:* The specification explicitly requires support for the approved Report definitions that establish the expected reporting scope.

#### FR-194 - Clone Report Definitions

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D12

The system shall allow authorized staff to clone an existing Report or Template into a new Report definition. Cloning shall copy the source definition sufficiently to create a variant without changing the original. The new definition shall be independently editable and stored.

*Priority rationale:* Cloning improves reuse and protects standard definitions, but staff can otherwise recreate a variant manually.

#### FR-195 - Cross-Tabulation And Pivoting

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D14, D20

The system shall support cross-tabulation and pivot-style analysis of Report data across terminal, Branch, System, hour, Patron age range, Patron type, and Patron location. Staff shall be able to summarize data by selected dimensions and inspect the resulting aggregated values. The capability may be provided interactively within the reporting tool or through pivot-table-style Report output.

*Priority rationale:* Cross-tabulation is repeatedly requested for analysis across operational dimensions, although basic Reports remain usable without it.

#### FR-196 - Edit Canned Report Displays

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall allow administrators or other authorized staff to edit the display fields of a Canned Report without changing its underlying selection logic. Staff shall be able to add or remove permitted display fields, such as shelving location. The resulting Canned Report shall present the configured display fields when executed.

*Priority rationale:* Adjustable display fields are useful for local reporting needs, while the underlying Canned Report can otherwise remain usable.

#### FR-197 - Picklist Query Values

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12

The system shall provide picklists of valid values when staff compose Query criteria. Staff shall be able to select a value from the applicable picklist instead of entering it manually. The selected value shall be retained as part of the Query criteria.

*Priority rationale:* Picklists reduce entry errors and simplify Query construction, but manual entry provides a temporary workaround.

#### FR-198 - Regular Expression Queries

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D14

The system shall support regular expression matching in Query criteria for advanced string and pattern searches. The Query interface shall provide a selectable list or drop-down of available regular expressions where applicable. A Query using a regular expression shall execute and return records matching the specified pattern.

*Priority rationale:* Advanced pattern matching is explicitly requested for complex reporting but is less essential than basic Query capabilities.

#### FR-199 - Reusable Report And Query Definitions

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D04, D10, D14, D15, D20

The system shall allow authorized staff to save Report and Query definitions for reuse across sessions. A saved definition shall retain its fields, criteria, formatting, and other execution parameters needed to rerun it without rebuilding the definition. Staff shall be able to reuse saved definitions for recurring reporting and transfer-selection work, and acceptance shall verify that permitted definitions can be saved and executed later with their criteria intact.

*Priority rationale:* Repeated Report and transfer-selection work is explicitly requested, although staff can temporarily recreate definitions manually.

### 5.17 Report Export

#### FR-200 - Explicit Null And Blank Values

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14, D19, D20

The system shall include null and blank field values explicitly in Report results when the corresponding fields are selected. It shall not implicitly omit or hide records or field values solely because a selected field is null or blank. Filters shall continue to apply according to their defined criteria, while null and blank values that satisfy those criteria remain represented in the result. Acceptance shall verify that records containing null or blank selected fields retain visible, distinguishable representations in generated and exported results.

*Priority rationale:* Four source documents request complete visibility of null and blank values, making this important for reliable analysis and record counts.

#### FR-201 - Multiple Report Export Formats

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14, D19, D20

The system shall export Reports in Excel, HTML, and CSV formats. The formats shall support web presentation, reliable data exchange, spreadsheet-based analysis, and business-user workflows. Each format shall be selectable for a generated Report and shall contain the Report's result data. Export acceptance shall verify that the resulting files or rendered output can be opened or consumed in the corresponding format.

*Priority rationale:* Multiple source documents request these formats, and the meeting record explicitly identifies Excel, HTML, and CSV as required.

#### FR-202 - Email Report Results

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14, D20

The system shall allow authorized Report users to specify one or more email recipients for generated Reports. It shall deliver results either on demand or after a scheduled Report execution, using the selected supported export format. The system shall preserve the generated result and identify delivery failures when email delivery cannot be completed.

*Priority rationale:* Email delivery is explicitly requested by multiple sources and provides an important alternative to retrieving results through the web interface.

#### FR-203 - MARC Values Per Record

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D20

The system shall extract selected MARC values from Bibliographic Records and present them on a single Report row per Bibliographic Record. The output shall retain the association between each selected value and its record, with repeated values combined according to the Report's defined representation rather than creating extra rows by default. Acceptance shall verify that selected MARC fields are extracted correctly and that each record occupies no more than one result row unless repetition is explicitly requested.

*Priority rationale:* Single-row MARC extraction supports important catalog analysis but is less foundational than core Item and quality Reports.

#### FR-204 - Text File Report Filtering

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall allow an authorized Report user to upload a text file containing identifiers such as barcodes or TCNs. It shall use the identifiers from the uploaded file as filter input for a Report. The system shall apply the resulting identifier set to the selected field and produce results for matching records. Acceptance shall verify that a file containing known identifiers returns the corresponding records and excludes records whose identifiers are absent from the file.

*Priority rationale:* Two sources request this capability to support large filter lists, although it is an efficiency feature rather than a prerequisite for ordinary Report filtering.

#### FR-205 - Deduplicated Excel Results

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D20

The system shall produce Excel exports with one row for each distinct result identified by the Report's result definition. It shall not introduce duplicate rows through the export process or through repeated values in unrelated joined fields. Legitimate repeated rows shall remain only when the Report definition identifies them as distinct results. Acceptance shall compare the Excel export with the defined Report result identity and verify that export processing does not create unintended duplicates.

*Priority rationale:* Clean Excel output is useful for analysis but is requested by only one source and can often be mitigated through Report design or spreadsheet cleanup.

### 5.18 Report Operations

#### FR-206 - Predefined Board Executive Reports

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D18

The system shall provide predefined Reports for library boards and executive stakeholders without requiring staff to design them ad hoc. These Reports shall include basic statistics needed for applicable state reporting, including the Georgia Annual Report and Application for State Aid. The predefined Reports shall be available for governance and external-consumer information needs.

*Priority rationale:* Multiple sources explicitly require these core governance and state-reporting Reports.

#### FR-207 - Systemwide Statistical Reports

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D17

The system shall enable the Global System Administrator to generate statistical Reports for the entire System. The Reports shall support systemwide and consortium-level analysis across the associated Branches. Access to this capability shall be available to the Global System Administrator in accordance with the administrator's responsibilities.

*Priority rationale:* Systemwide statistical reporting is explicitly required for administration of the entire System.

#### FR-208 - Three Reporting Interfaces

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide distinct interfaces for Canned Reports, on-demand Reports, and open Template reporting. The interfaces shall support different levels of staff expertise and reporting needs. Each interface shall be identifiable as a separate reporting mode and shall be available from the reporting functionality.

*Priority rationale:* The three-interface model is explicitly requested in multiple sources to serve different reporting use cases.

#### FR-209 - Comparative Period Columns

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall support Report columns that compare the current reporting period with prior periods. A Report shall be able to show the previous month's Circulation, the corresponding prior-year month, and percentage differences for the applicable comparisons. The comparison periods and percentage calculations shall be identifiable in the Report output.

*Priority rationale:* Comparative period analysis is explicitly requested and materially supports interpretation of Report results.

#### FR-210 - Executive Reports Interface

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D17, D18

The system shall provide an Executive Reports Interface tailored to executive and board information needs. The interface shall include the Reports identified by the responsible working group as required for executive use. Staff shall be able to access the compiled executive Report set through that interface.

*Priority rationale:* The working group explicitly requested an executive interface and compiled Report set, but general reporting remains a temporary fallback.

#### FR-211 - Management Reporting Tools

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D17

The system shall provide Reports and analysis tools for managers, administrators, and staff. These tools shall support planning, evaluation, and operational oversight. The Reports shall present library data in a form that enables those stakeholders to review performance and inform management decisions.

*Priority rationale:* Management reporting supports broad stakeholder needs and is explicitly identified as a purpose of the reporting capability.

#### FR-212 - On-Demand Report Criteria

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide an on-demand Report interface that starts from preset Reports while allowing staff to modify selection criteria before execution. Staff shall also be able to adjust the display options for the resulting Report. The system shall apply the modified criteria and display options to the generated Report.

*Priority rationale:* On-demand modification is an important reporting capability, although predefined Reports provide a temporary workaround.

#### FR-213 - Open Template Reporting

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide an open Template reporting interface for power users to create reusable Report definitions. The interface shall expose attributes associated with Circulation, Items, Patrons, Fines, and Bibliographic Records for filtering and display selection. A user shall be able to select the desired attributes and save a reusable Template.

*Priority rationale:* Open Template reporting is explicitly requested for advanced and reusable reporting, but basic Canned Reports provide a temporary workaround.

#### FR-214 - Report Quick Access Descriptions

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide a quick-access interface for Reports and Templates. Each Canned Report or Template title shall display a description when the user hovers over it. The description shall help the user identify the purpose of the selected Report or Template before opening or running it.

*Priority rationale:* Multiple sources request this usability feature to help staff identify Reports quickly, though Reports remain usable without it.

#### FR-215 - Report Result Identification

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall include the Report name in each Report result. It shall also include the date selection criteria used to produce the result. These identifiers shall appear at the top or bottom of the result so staff can identify the Report and its date range without reopening the criteria.

*Priority rationale:* Result identification is explicitly requested and helps staff interpret and use Reports correctly.

#### FR-216 - Selectable Report Data

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall allow a user to select the data elements to include in a Report. The selection interface shall present the available data elements as individually selectable options. The generated Report shall contain the data elements selected by the user and omit unselected elements.

*Priority rationale:* Selectable data elements improve Report usability and are explicitly requested, but fixed Reports provide a limited workaround.

#### FR-217 - Current Data Reporting

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall support generating Reports from current data when staff require up-to-date results. The system shall identify the data currency or retrieval time associated with a Report generated using current data. A Report requested for current data shall use the latest data available to the reporting service at execution time.

*Priority rationale:* Current-data reporting is useful for operational decisions but is requested by only one source and may have a temporary manual workaround.

### 5.19 Report Permissions

#### FR-218 - Ad Hoc Data Access Control

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12

The system shall allow administrators to permit or restrict staff from running ad hoc Reports against specified sets of data. These restrictions shall be assignable by Role, group, or other administrator-defined permission scope. A staff member shall be prevented from executing an ad hoc Query when its data scope is outside the permissions granted to that staff member.

*Priority rationale:* Multiple sources require restrictions on ad hoc access to specific data, which is necessary to prevent unauthorized data exposure.

#### FR-219 - Destructive Operation Permissions

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D06

The system shall restrict purge and other destructive operations through Role-based permissions. Only authorized staff shall be able to delete records or perform bulk status changes through Reports or related administrative functions. The system shall deny such operations to staff whose assigned Role lacks the required permission.

*Priority rationale:* Restricting destructive operations is explicitly required to prevent accidental or unauthorized bulk changes.

#### FR-220 - Fine-Grained Report Permissions

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D14, D20

The system shall provide distinct, fine-grained permissions for creating, editing, cloning, running, viewing, and modifying Reports, Queries, and Templates. Administrators shall be able to separate Report creation and maintenance permissions from Report execution permissions and control access to the Query tool and its features. Adding a Canned Report or Template shall require the corresponding permission.

*Priority rationale:* Fine-grained control over Report and Query authoring and execution is repeatedly requested and is essential for governance and data protection.

#### FR-221 - Predefined Report Roles

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D17, D19

The system shall support predefined Roles with appropriate access to Reports and administrative functions, including Global Administrator, Local Administrator, Library Manager, Staff, and Patron access levels. Global Administrator access shall cover the full reporting system, while Local Administrator, Library Manager, and Staff access shall be limited according to their responsibilities and approved permissions. The system shall permit the defined role model to distinguish branch-level administration, approved Report execution, limited Template modification, and indirect Patron access.

*Priority rationale:* The working-group decisions define role semantics that are necessary for consistent access control across the System.

#### FR-222 - Role Assignment Administration

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D13, D16, D19

The system shall provide an administrative interface for creating, modifying, assigning, and managing Roles and their permissions. When an administrator changes a staff member's Role, the system shall automatically apply the permissions associated with the new Role. Role and permission administration shall support straightforward changes through Role assignment rather than requiring multiple individual permission edits.

*Priority rationale:* Multiple sources explicitly require simple administrative management and automatic permission changes when staff responsibilities change.

#### FR-223 - Role-Based Access Control

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D13, D16, D18, D19

The system shall control staff rights and privileges through security groups and Roles. It shall assign permissions to individuals, defined workgroups, and arbitrary staff groups, and shall determine those permissions from the assigned Role when a staff member accesses the system. The access-control mechanism shall restrict Reports and related operations according to the assigned permissions.

*Priority rationale:* Role-based access control is explicitly requested by multiple sources and is foundational to secure Report access.

#### FR-224 - Table And Field Access

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall allow administrators to control staff access to database tables and individual fields used by Reports and Queries. The access rules shall support granting or denying access by Role or group. Reports and Queries shall not expose restricted tables or fields to staff who lack the corresponding permission.

*Priority rationale:* Table- and field-level controls are explicitly required to enforce data security and privacy.

#### FR-225 - Permission-Based Filter Restrictions

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D14

The system shall allow administrators to restrict which filters staff may use in Reports and Queries based on Roles or permissions. A staff member shall be unable to select or apply a restricted filter when the associated permission has not been granted. The restriction shall support protection of sensitive criteria as well as the resulting data.

*Priority rationale:* Filter restrictions provide an additional privacy control requested by the reference requirements, although broader data permissions may provide a temporary workaround.

#### FR-226 - Shared Report Folders

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D14, D20

The system shall allow administrators to create shared folders or workspaces for saved Reports and Templates. Administrators shall be able to grant or deny specific staff members or groups permission to access or run Reports in each shared folder. Shared folders shall support controlled sharing of Report definitions and Templates without granting unrestricted access to all Reports.

*Priority rationale:* Shared Report folders are requested by several sources and provide important group-level governance, but individual access controls can provide a temporary workaround.

### 5.20 Report Scheduling

#### FR-227 - Cancel Report Execution

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14, D19, D20

The system shall allow an authorized user to cancel a Report that is scheduled or currently running. The execution process shall check for cancellation signals during processing and terminate the Report within a timely, system-defined interval. The system shall update the Report status to indicate that cancellation occurred and shall release resources that are no longer needed.

*Priority rationale:* Cancellation is needed to correct scheduling errors and control long-running Reports that consume shared resources.

#### FR-228 - Flexible Report Scheduling

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14, D20

The system shall allow staff to schedule Reports for immediate execution or for hourly, daily, weekly, monthly, or yearly recurring execution. Recurring schedules shall execute automatically according to the selected frequency. Scheduled Reports shall support the available output format choices required for the resulting Report so scheduling can serve varied operational needs.

*Priority rationale:* Immediate and recurring execution at common frequencies is a core scheduling capability requested by multiple sources.

#### FR-229 - Prioritize And Preempt Reports

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D14

The system shall support configurable priority levels for Report jobs or Report types in the Report Queue. An authorized administrator shall be able to configure priorities so urgent Reports are processed ahead of eligible lower-priority or resource-consuming Reports. The system shall allow an authorized administrator to preempt a lower-priority Report that is running when a higher-priority Report requires execution, and shall mark the interrupted Report as preempted for operational follow-up.

*Priority rationale:* The source identifies urgent Report prioritization as crucial and explicitly includes preemption to address immediate reporting needs.

#### FR-230 - Report Queue Visibility

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D12, D14, D18, D20

The system shall provide staff with a queue view for submitted Reports. The view shall show submission time, queue position, number of Reports ahead, and a shared execution state of queued or waiting, processing or running, completed, or failed. The interface shall provide available progress information so staff can understand expected wait and completion state.

*Priority rationale:* Queue position and processing-state visibility are repeatedly requested and are essential for monitoring asynchronous Report execution.

#### FR-231 - Edit Recurring Report Schedules

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall allow an authorized user to edit an existing recurring Report schedule. The user shall be able to add or remove Report selections and modify the email recipient list associated with the schedule. Changes shall apply to subsequent executions without requiring the recurring schedule to be recreated.

*Priority rationale:* Editing schedules is important for ongoing operations, although users can temporarily create a replacement schedule.

#### FR-232 - Batch Report Execution

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall allow staff to select multiple Reports for execution as one batch. The selected Reports shall be submitted for execution together rather than requiring separate submissions. The system shall support presenting the resulting Reports within a single document when that output arrangement is selected.

*Priority rationale:* Batch execution can reduce repetitive work, but users can otherwise submit Reports individually.

#### FR-233 - Canned Report Scheduling Interface

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall provide an interface containing the Canned Reports delivered with the product. Staff shall be able to select a Canned Report and run it immediately or schedule it for recurring execution. The interface shall identify the available Canned Reports and expose the execution choice for each selected Report.

*Priority rationale:* Pre-written Reports are useful for operational work, but this capability is less central than general scheduling and queue control.

#### FR-234 - Relative Date Report Execution

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall allow a Canned Report to use relative date ranges when it executes. Supported relative ranges shall include yesterday, last week, last month, and last year. The resulting date range shall be calculated from the execution date so the same schedule can be reused over time.

*Priority rationale:* Relative dates simplify recurring operational Reports but are a convenience beyond basic Report execution.

#### FR-235 - Report Delivery Address Book

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D14

The system shall provide an address book for storing and selecting regularly used email addresses for Report delivery. Staff shall be able to choose saved recipients when configuring an emailed Report or recurring schedule. The address book shall reduce repeated manual entry of recipient addresses.

*Priority rationale:* Saved recipients improve convenience, but users can enter email addresses manually when the address book is unavailable.

### 5.21 Transit Monitoring

#### FR-236 - Branch Missing Damage Reports

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D05, D10, D15, D18

The system shall provide Reports listing missing and damaged Items for each Branch. Branch staff and managers shall be able to use the Reports to monitor collection health, support local inventory work, and investigate losses or claims. The Report shall identify the relevant Item and its Branch so the results can be verified against inventory records.

*Priority rationale:* Multiple sources identify branch-level missing and damaged Item reporting as essential for accountability, inventory, and claims work.

#### FR-237 - Combined Transit Direction Report

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D05, D10, D15

The system shall provide a combined Report containing Items in Transit to and from Branches. Users shall not need to run separate Reports for the two Transit directions. The combined results shall support front-line staff in tracking and following up on Items moving between Branches.

*Priority rationale:* Multiple working-group sources explicitly require one combined Transit Report to reduce operational effort and simplify follow-up.

#### FR-238 - Missing Damage Counts

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D05

The system shall present numeric counts of missing and damaged Items in the relevant Reports. Counts shall be available for the selected scope and criteria, including Branch and date range where applicable. Users shall be able to use the counts to support inventory audits and accountability reviews.

*Priority rationale:* Numeric summaries are explicitly required for inventory auditing and are a core part of accountable loss reporting.

#### FR-239 - Periodic Overdue Transit Reports

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D05, D10, D15

The system shall generate a recurring Report of Items whose Transit duration exceeds a configurable threshold. The Report shall support periodic scheduling and scopes by Branch and by System, and shall identify each Item and its Transit information. The default threshold shall be seven days unless an administrator configures another value.

*Priority rationale:* Overdue Transit monitoring across Branches and the System is a core operational need, and the sources explicitly require periodic execution and a configurable threshold.

#### FR-240 - Transit Reports By Branches

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D18

The system shall provide Transit Reports that identify both the sending Branch and the destination Branch for each Item. Users shall be able to group or filter results by sending Branch and by destination Branch. These views shall support coordination of outbound shipments and delivery between Branches and central services.

*Priority rationale:* Movement between Branches cannot be operationally monitored without identifying both ends of each Transit, and multiple sources request these views.

#### FR-241 - Exportable Operational Reports

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D05

The system shall allow relevant missing, damaged, and Transit Reports to be delivered in a printable or commonly exportable format. Exported results shall preserve the selected records, fields, and report scope. Staff shall be able to use the resulting output for inventory audits and collection management decisions.

*Priority rationale:* Export or print output is clearly needed for audits and management work, while on-screen Reports provide a temporary alternative.

#### FR-242 - Filter By Item Status

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D05

The system shall allow Reports to filter Items by one or more configured status values. Status values shall include, where tracked, missing, lost, and long overdue. Users shall be able to combine status filtering with Branch or other available Report criteria.

*Priority rationale:* Status filtering supports operational identification of problematic Items and is clearly requested, but basic reports can temporarily be reviewed without it.

#### FR-243 - Item Condition Notes

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D05

The system shall include Item condition notes in missing and damaged Item Reports. The notes shall preserve descriptive information such as water damage or vandalism. Staff shall be able to review these notes alongside the affected Item and Branch.

*Priority rationale:* Condition details are important for identifying damage causes, but the core missing and damaged Report remains useful without them.

#### FR-244 - Missing Damage Date Filters

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D05

The system shall allow users to filter missing and damaged Item Reports by a selected date range. Supported ranges shall include user-defined dates and commonly used periods such as the last 30 days or last quarter. The resulting Report shall contain only records whose relevant missing or damage date falls within the selected range.

*Priority rationale:* Date filtering is repeatedly requested to support trend analysis, although a complete unfiltered Report provides a temporary workaround.

#### FR-245 - Reports By Bibliographic Record

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D05

The system shall allow missing and damaged Item Reports to group or aggregate results by Bibliographic Record. The grouped results shall show the number of affected Items for each Bibliographic Record. Staff shall be able to use this view to identify works that are repeatedly lost or damaged.

*Priority rationale:* Grouping by Bibliographic Record supports collection decisions and pattern detection but is not required for basic loss accountability.

#### FR-246 - Sort Transit Items By Due Date

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D05

The system shall allow users to sort the Transit Report by due date. The Report shall support ordering Items so that the oldest or most urgent due dates can be reviewed first. This ordering shall help front-line staff prioritize follow-up on delayed Items.

*Priority rationale:* Due-date ordering directly improves follow-up efficiency, although staff can temporarily prioritize Items using unsorted results.

#### FR-247 - Transit Items With Holds

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall produce a periodic Report of Items in Transit that have an outstanding Hold. The Report shall identify the Item, its Transit status, the relevant destination Branch, and the outstanding Hold. Staff shall be able to use the Report to coordinate delivery of Items needed to fulfill Holds.

*Priority rationale:* Monitoring held Items in Transit supports timely service and coordination, but it is narrower than the core Transit monitoring Report.

### 5.22 Uncataloged Materials

#### FR-248 - Uncataloged Item Inventory

**Priority:** Must &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D15

The system shall represent, locate, and manage uncataloged Items as inventory before their Bibliographic Records are completed. Staff shall be able to record uncataloged shipments or Items, account for them, and include them in applicable operational Reports without requiring completed Bibliographic Records. Acceptance shall verify inventory control for materials such as paperbacks and children's board books throughout the uncataloged period.

*Priority rationale:* Tracking uncataloged Items is essential for accountability and daily management before cataloging is complete.

#### FR-249 - Report Uncataloged Item Use

**Priority:** Should &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10, D15

The system shall record and Report how uncataloged Items are used before full cataloging. Reports shall support applicable usage and Circulation measures for individual uncataloged Items or relevant groups, including non-cataloged in-house use counts by month. Acceptance shall verify that staff can retrieve these usage measures independently of completed Bibliographic Records.

*Priority rationale:* Usage analysis is explicitly requested to evaluate uncataloged material, but it is secondary to basic inventory control.

#### FR-250 - Report Cataloged In-House Use

**Priority:** Could &nbsp;·&nbsp; **Type:** functional &nbsp;·&nbsp; **Sources:** D10

The system shall record and Report in-house use counts for cataloged Items. Staff shall be able to retrieve these counts to assess physical Item use within Branch facilities. Acceptance requires that a Report can distinguish cataloged in-house use and present the corresponding counts.

*Priority rationale:* This is a valid usage-reporting need but is less central to uncataloged material and is requested by only one candidate.

## 6. Non-functional requirements and constraints

### 6.1 Authentication Sessions

#### CON-001 - Optional Card Reader Support

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D13

The system shall support card-based staff login without requiring card-reader hardware for basic operation. It shall operate at Branches that do not have card readers, using username-and-password authentication where card hardware is unavailable. Deploying or enabling card-reader hardware shall therefore remain optional.

*Priority rationale:* The system must remain usable across Branches with differing infrastructure and must not make card-reader installation a prerequisite for operation.

### 6.2 Collection Capacity

#### NFR-001 - At-A-Glance Capacity Decisions

**Priority:** Should &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D02

The system shall present capacity information so staff can understand the status of Branches quickly when deciding where to allocate resources or move Items. The presentation shall expose the key capacity indicators without requiring users to inspect multiple separate views. A representative user shall be able to identify the relevant Branch status from the overview during normal operational use.

*Priority rationale:* Rapid interpretation is important for daily operational decisions, although detailed Reports remain a temporary alternative.

#### NFR-002 - Large Location Usability

**Priority:** Should &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D02

The system shall keep the capacity interface usable and comprehensible when a System contains a large number of Branches. It shall provide mechanisms such as grouping, filtering, or aggregation to prevent the overview from becoming excessively cluttered. The interface shall remain operable for a location count of at least 286 Branches.

*Priority rationale:* The stated large-location scenario can impair daily use and requires explicit usability safeguards, though it affects larger Systems most directly.

#### NFR-003 - Outlier Identification Presentation

**Priority:** Should &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D03

The system shall present Shelf Space comparison results in a visual or tabular form that makes outliers between space allocation and use easy to identify. The presentation shall preserve the underlying percentage values so users can verify why a result is an outlier. This capability shall apply to the selected genre, format, Branch, System, and date range.

*Priority rationale:* Quickly identifying space-versus-use mismatches supports the stated management purpose, while manual inspection remains possible.

#### CON-002 - Use Acquisition Dates

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D01

The system shall use the existing Item acquisition date field when calculating new acquisitions and historical collection volume. Reports shall rely on the stored acquisition date rather than requiring a separate acquisition-date data source. The field shall support date-based volume calculations.

*Priority rationale:* The existing acquisition date is the identified authoritative data source for acquisition and historical volume calculations.

### 6.3 Deletion Auditing

#### NFR-004 - Retain Deletion Audit Logs

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D07

The system shall retain deletion and denied-deletion audit logs for a period and in a manner suitable for applicable audit, legal, and data-retention requirements. Retained logs shall remain available as evidence of how deletion activities were handled. The retention behavior shall support libraries that must demonstrate compliance with their retention schedules.

*Priority rationale:* Preserving deletion evidence is necessary for legal and audit obligations explicitly identified by stakeholders.

#### CON-003 - Persist Deletion Audit Records

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D07

The system shall capture deletion events through a database trigger that writes an audit record at the time of deletion. The audit records shall be stored in a database audit table. The table shall support reliable querying and aggregation of deletion events. The implementation shall ensure that deletion auditing does not depend on a user remembering to create a separate log entry.

*Priority rationale:* The source requirements explicitly mandate database-triggered persistence to make deletion capture reliable.

### 6.4 Documentation Accessibility

#### NFR-005 - Accessible User Interfaces

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D10, D14, D16, D18, D19

The system shall comply with applicable legal accessibility requirements, including Section 508 where applicable to the System. All reporting and other staff-facing interfaces, including the help system, shall support common assistive technologies such as screen readers and screen magnification software. Accessibility shall be verifiable through conformance evaluation and practical operation with technologies such as JAWS, NVDA, and ZoomText.

*Priority rationale:* Accessibility is described as mandatory and non-negotiable for the public institution, and multiple sources require assistive-technology support and compliance.

#### CON-004 - Adapted Requirements Foundation

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D17

The system shall be specified using the King County and Galecia Group draft Software Requirements Specification as a foundation, adapted to the needs of the PINES System. The adapted documentation shall preserve relevant foundation content while incorporating approved PINES-specific requirements. The resulting specification shall be identifiable as the project-specific version used for implementation.

*Priority rationale:* The working group explicitly decided to use and adapt the existing specification as the foundation for the project requirements.

#### CON-005 - Complete Data Specifications

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D10, D18, D19

The system shall be accompanied by complete data specifications and data dictionaries for authority, Bibliographic Record, order, Item, Hold, and other records accessed or maintained by Management Processes. The specifications shall identify field names, data types, relationships, and other information needed to construct effective Queries. The documentation shall cover all data exposed to staff for reporting and analysis.

*Priority rationale:* Complete data specifications are explicitly demanded as a high-priority foundation for effective Query development.

#### CON-006 - High-Level Process Documentation

**Priority:** Should &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D10, D18, D19

The system shall be accompanied by thorough high-level descriptions of major data and reporting processes. The documentation shall include Bibliographic Record import and export, validation against authority sources, and standard Reports. The descriptions shall explain relevant data flows sufficiently for staff and developers to understand and verify process behaviour.

*Priority rationale:* Process documentation is explicitly requested by multiple sources and is important for understanding system behaviour, but core operation can continue with temporary documentation workarounds.

#### CON-007 - Readable Requirements Specification

**Priority:** Should &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D17

The system shall be specified by requirements documentation that is understandable to library managers and staff as well as software project managers and developers. The documentation shall balance readable explanations for non-technical readers with sufficient precision for implementation and verification. Acceptance of the documentation shall be assessed by review from both audience groups.

*Priority rationale:* The working group explicitly identifies both managerial and development audiences, making readable yet precise documentation important for successful implementation.

#### CON-008 - Library Terminology Assumption

**Priority:** Could &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D17

The system shall be documented for readers who are assumed to understand common library services and processes. The requirements documentation need not define established library terminology, but it shall provide definitions for project-specific terms, ambiguous concepts, and technical details needed for implementation or verification. Documentation reviews shall confirm that omitted definitions do not prevent the intended audiences from interpreting requirements.

*Priority rationale:* This is an explicitly recorded documentation convention with limited operational impact and can be supplemented by a glossary or reviewer clarification when needed.

#### CON-009 - Defer Detailed Interface Specification

**Priority:** Won't &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D17

The system shall defer detailed user-interface and data-structure specifications during the initial requirements phase. The project shall prioritize documenting functional requirements before completing those specifications. The project shall refine the deferred specifications later through iterative prototyping.

*Priority rationale:* The source explicitly states that detailed interface and data-structure specification is deferred until a later phase.

### 6.5 Financial Reporting

#### NFR-006 - Protect Archived Financial Privacy

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D10, D12

The system shall archive financial Transaction data in a form that protects Patron privacy while satisfying applicable legal and audit retention requirements. Archived data shall not retain personally identifiable information when that information is not required for compliance. The retained data shall remain useful for authorized financial and aggregate statistical reporting.

*Priority rationale:* Protecting Patron personally identifiable information during legally required retention is an explicit privacy and compliance obligation.

#### NFR-007 - Update Payments Immediately

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D11

The system shall update the applicable financial records when a Patron payment is recorded. The updated payment, account balance, and related Reports shall become available without a material operational delay after the payment is accepted. This behavior shall apply to payments recorded at the front desk and equivalent payment interfaces.

*Priority rationale:* Immediate balance and payment visibility is necessary for reliable front-desk operations and accurate financial reporting.

#### NFR-008 - Edit Financial Information

**Priority:** Should &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D10

The system shall allow authorized staff to update financial information attached to Patron and Item records. The editing interface shall support routine corrections without requiring direct database manipulation. Changes shall preserve the resulting financial record for subsequent reporting and audit.

*Priority rationale:* Staff need efficient correction of financial information, although a controlled manual workaround may exist.

#### CON-010 - Meet Financial Audit Requirements

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D10, D11

The system shall produce financial Reports and preserve financial data in accordance with applicable accounting practices and state, county, and municipal auditing requirements. Compliance shall apply to both generated Reports and archived financial data. The resulting records shall support review and audit of financial activity.

*Priority rationale:* Accounting and audit compliance is an explicit legal and operational obligation.

#### CON-011 - Retain Financial Transaction History

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D10, D11, D12, D20

The system shall retain detailed financial Transaction history for the period required by applicable law and audit practice, with the retention period configurable by authorized administrators where permitted. The system shall support a legally specified period such as seven years rather than imposing a shorter fixed period. Monthly and annual aggregate transaction information shall be retained indefinitely for reporting and compliance.

*Priority rationale:* Legally required financial retention and indefinite aggregate retention are necessary for audit compliance and longitudinal reporting.

### 6.6 Item And Catalog Reports

#### NFR-009 - Consortium Scale Support

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D10, D18

The system shall support operation across a large consortium with approximately 286 Branches, 17 million annual Circulation transactions, and processing of more than 900,000 Items per year. It shall maintain usable reporting and administrative operation at this scale. Acceptance shall include successful handling of the stated location, transaction, purchasing, and processing volumes.

*Priority rationale:* The stated consortium scale is essential for the target System to operate acceptably.

### 6.7 Item Transfers

#### NFR-010 - Ensure Transaction-Safe Updates

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D04

The system shall apply batch Item-location updates within transaction-safe operations that preserve database integrity. If an update fails, the system shall roll back the affected operation so that it does not leave a partially updated transfer. Acceptance shall include inducing an update failure and verifying that the affected Items retain a consistent pre-operation or fully committed state.

*Priority rationale:* Partial location updates could lose control of Items, so transaction safety is essential for every batch transfer.

#### NFR-011 - Log Transfer Operations

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D04

The system shall record every transfer operation in an Audit Log. Each record shall include the initiating staff identity, the affected Items, source and destination locations, and the operation timestamp. Acceptance shall include retrieving a complete log entry after a transfer is initiated and completed.

*Priority rationale:* Transfer accountability and traceability are explicitly required for auditing and operational investigation.

#### NFR-012 - Scale Large Transfer Updates

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D04

The system shall process large batch transfers efficiently, including collections containing millions of Items, without excessive database locking or unacceptable performance degradation. Processing shall support smaller batches or chunks when needed to limit lock duration. Acceptance shall include measuring a large transfer under representative load and verifying that processing completes without excessive locking or service disruption.

*Priority rationale:* The stated collection size and explicit locking concern make scalable transfer processing necessary for an acceptable system.

#### CON-012 - Reuse Existing Query Builder

**Priority:** Should &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D04

The system shall integrate transfer candidate selection with the existing Query builder. Transfer staff shall be able to use the builder's supported criteria and selection capabilities without maintaining a separate transfer-only query mechanism. Acceptance shall include creating or running a transfer Query through the existing builder and passing its results to the transfer workflow.

*Priority rationale:* Reusing the existing Query builder reduces duplicate functionality and implementation effort while preserving the required selection capability.

### 6.8 Patron Demographics

#### NFR-013 - Anonymized Demographic Reporting

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D10, D20

The system shall anonymize data used for demographic Reports and statistics so that the outputs do not expose personally identifiable information. Aggregation shall prevent a demographic result from directly identifying an individual Patron. Acceptance shall verify that demographic outputs omit or remove identifying Patron details.

*Priority rationale:* Protecting Patron privacy is explicitly required by multiple sources and is essential for acceptable demographic reporting.

#### CON-013 - Supported Web Browsers

**Priority:** Should &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D10, D16, D18

The system shall support browser-based access through Microsoft Internet Explorer version 6.0 and later and Mozilla Firefox version 2.0 and later when web-browser access is used. Supported browser operation shall include the reporting functions available to the user. Acceptance shall verify access and execution of the relevant reporting workflows in each specified browser family and version range.

*Priority rationale:* Browser compatibility is an explicit library standard and is needed for practical access to the reporting system.

### 6.9 Patron Inactivity

#### NFR-014 - Large Patron Dataset Performance

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D09

The system shall process inactive Patron Reports acceptably on large datasets, including an example scale of approximately 3.5 million Patron records. The implementation shall use appropriate query optimization, indexing, aggregation, or caching techniques. Performance testing shall demonstrate that the Report remains operationally usable at the target scale.

*Priority rationale:* The stated dataset scale can make the core inactive-Patron operation unusable without explicit performance engineering.

#### NFR-015 - Background Inactivity Processing

**Priority:** Should &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D09

The system shall execute the inactive Patron Report as a background process when its data volume or activity aggregation could affect interactive use. The system shall cache or otherwise retain completed results for retrieval without repeating the full calculation unnecessarily. Processing shall not block normal interactive System operations.

*Priority rationale:* The source identifies the query as potentially expensive, making background execution and result reuse important for operational performance.

#### CON-014 - Qualifying Activity Calculation

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D09

The system shall determine each Patron's most recent qualifying activity from Circulation and electronic activity sources. Electronic activity shall include OPAC or Patron account logins, online Hold placement, online renewals, and digital collection access when integrated. The system shall combine activity stored in separate source tables and use the resulting latest activity date to apply the Inactivity threshold. The calculation shall be based on recorded Transactions or activity records rather than a manually maintained status.

*Priority rationale:* Accurate identification of inactivity depends on combining all specified activity sources and applying the threshold consistently.

#### CON-015 - Calculate Age From Birthdate

**Priority:** Should &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D08

The system shall calculate a Patron's age from the recorded birthdate when evaluating an age range. The calculation shall occur at Query or Report execution time so that age grouping reflects the current date. The system shall use the calculated age rather than relying on a permanently stored age value.

*Priority rationale:* Current age grouping requires a consistent calculation from the authoritative birthdate field.

#### CON-016 - CSV Report Export

**Priority:** Should &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D09

The system shall allow the inactive Patron Report to be exported in CSV format. The exported file shall contain the selected Report fields and records in a machine-readable structure suitable for outreach or third-party processing. Export shall respect the Report's filters and exclusions.

*Priority rationale:* CSV export is explicitly requested to support operational outreach and integration with external tools.

### 6.10 Platform Integration

#### NFR-016 - Non Disruptive Reporting

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D10, D16, D19

The system shall allow searches and Reports to execute during open hours without materially disrupting protected production workflows. Reporting workloads shall be isolated or controlled so complex queries do not tie up shared resources or reduce normal responsiveness of the circulation client, OPAC, or other system functions. Acceptance testing shall demonstrate normal staff and Patron responsiveness while representative complex Reports are running.

*Priority rationale:* The sources consistently identify uninterrupted circulation-client and OPAC operation during open-hours reporting as essential.

#### NFR-017 - Training Data Isolation

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D19

The system shall ensure that the training environment cannot put production data at risk. It shall provide data isolation, sanitized data, test data, or an equivalent control that prevents training activities from changing or exposing live operational data. Acceptance shall verify that staff can experiment in training without affecting production data.

*Priority rationale:* Preventing training activity from damaging or exposing production data is essential for safe operation.

#### NFR-018 - Discoverable Reports Interface

**Priority:** Should &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D20

The system shall provide a Reports interface with clear navigation, search, and discovery features. Staff shall be able to locate available Reports without relying on undocumented knowledge of the system. Usability evaluation shall verify that representative staff can find specified Reports using the provided interface.

*Priority rationale:* Staff explicitly report difficulty finding Reports, making discoverability important though a manual workaround may exist.

#### NFR-019 - Real-Time Reporting Capability

**Priority:** Should &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D20

The system shall support real-time or near-real-time Reports for selected operational use cases. Such Reports shall reflect live activity or changes within a defined, documented freshness interval. The interval shall be specified per applicable Report and verified using newly created or changed source data.

*Priority rationale:* Staff survey feedback requests current data for busy-period monitoring, although not every Report requires real-time freshness.

#### NFR-020 - Report Performance Under Load

**Priority:** Should &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D20

The system shall generate Reports within acceptable response times during peak operating hours. Performance targets shall be defined for representative Reports and tested under representative peak data and workload conditions. Report execution shall not remain excessively delayed solely because the System is busy.

*Priority rationale:* Peak-hour delays are a reported operational problem, but temporary scheduling or workload-management workarounds may exist.

#### CON-017 - Enterprise Infrastructure Compatibility

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D19

The system shall operate within the enterprise infrastructure supporting the Library Automation System. It may rely on available redundant servers, backup systems, and network connectivity rather than independently replacing those services. Acceptance shall verify deployment and operation using the supported enterprise infrastructure.

*Priority rationale:* Compatibility with the existing resilient infrastructure is necessary for deployment and operational continuity.

#### CON-018 - Enterprise Library System Integration

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D10, D17, D18

The system shall operate as an integrated component of an enterprise-level Library Automation System. It shall use and remain compatible with the enterprise system's general data structures and functionality rather than assuming an independent data model. Acceptance shall verify interoperability with the target enterprise services and data structures.

*Priority rationale:* Integration with the existing enterprise Library Automation System is required for the system to function in its target environment.

#### CON-019 - Normalized Relational Reporting

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D16, D19

The system shall execute reporting against the primary normalized relational database schema without requiring a separately maintained denormalized reporting schema or synchronized copy. Queries shall support complex joins across relevant relational data while treating the operational relational schema as authoritative. Acceptance shall verify that required Reports use the normalized schema, support representative complex joins, and do not depend on denormalized synchronization.

*Priority rationale:* The sources explicitly require reliable reporting against the authoritative relational schema while avoiding synchronization problems from denormalized copies.

#### CON-020 - Patron-Facing Scope Boundary

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D17

The system shall exclude day-to-day Patron-facing functions from its scope. Those functions shall remain the responsibility of the OPAC and circulation client rather than being implemented in the reporting system. Acceptance shall verify that the delivered system provides staff reporting capabilities without claiming responsibility for routine Patron-facing transactions.

*Priority rationale:* The stakeholder explicitly defines this boundary to prevent overlap with the OPAC and circulation client.

#### CON-021 - PostgreSQL Platform Compatibility

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D16, D19

The system shall be compatible with the PostgreSQL database platform used by PINES. It shall operate against the existing production database environment, including the currently identified PostgreSQL 8.3 platform where applicable. Acceptance shall verify deployment and reporting against the supported PostgreSQL environment.

*Priority rationale:* Compatibility with the existing PostgreSQL platform is required for deployment in the target environment.

#### CON-022 - Preserve OPAC Independence

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D10, D18, D19

The system shall remain separate from the OPAC and shall not constrain, alter, or require changes to OPAC functionality or features. Management and reporting capabilities shall not impose dependencies that reduce the OPAC's autonomy. Verification shall confirm that reporting changes can be deployed without modifying public-facing OPAC behavior.

*Priority rationale:* Multiple meeting records state that the reporting system must not constrain the public catalog, including an explicit statement that this is unacceptable.

#### CON-023 - Production Reporting Isolation

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D14, D16

The system shall separate reporting workloads from production operational processing so reporting Queries do not adversely affect transactional performance. It shall support a separate reporting database or a read-only reporting replica when required to offload reporting Queries from the primary database. Acceptance shall verify that reporting can execute through the separated architecture without directly burdening production operations.

*Priority rationale:* Protecting production transaction performance is essential for a system that shares infrastructure with operational services.

#### CON-024 - Relational Database Backend

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D10, D18, D19

The system shall use a fully relational database backend for storing and retrieving reporting data. Reporting and Query processing shall operate correctly against the relational data model used by the Library Automation System. Acceptance shall verify that required reporting functions work with the existing relational structure.

*Priority rationale:* A relational backend is explicitly required and is essential for compatibility with the existing Library Automation System data model.

#### CON-025 - Run On Existing Hardware

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D16

The system shall run acceptably on the existing central IT server class used by PINES. The target environment includes Red Hat Enterprise Linux 5 with dual quad-core processors and 32 GB of RAM. Deployment verification shall demonstrate supported operation and acceptable performance on that server class.

*Priority rationale:* Compatibility with the existing central infrastructure is necessary for deployment without an immediate hardware replacement.

#### CON-026 - Separated Development Training Environments

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D10, D14, D16, D18, D19

The system shall provide separate development, training, and production environments for report development, staff practice, and live operation. It shall support exporting and importing report Templates, permission settings, and other configuration from development or training into production. Acceptance shall verify that configuration can be migrated without directly modifying production during development or training activities.

*Priority rationale:* Separate environments and controlled configuration migration are repeatedly required to protect live operations and support safe deployment.

#### CON-027 - Standards-Compliant HTML Output

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D10, D16, D18, D19

The system shall produce standards-compliant HTML for web interfaces, Reports, and help content. The HTML shall validate against applicable W3C standards and use semantic structure, including alternative text and appropriate ARIA labels where needed. Output shall remain interoperable across supported browsers and assistive technologies.

*Priority rationale:* Standards-compliant and accessible HTML is explicitly marked high priority and is required across the system's web output.

#### CON-028 - Supported Client Access

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D10, D18

The system shall provide staff access to reporting functionality through at least one supported client environment: a web browser or a Windows-compatible client. The implementation shall document which option is supported and shall not require both client environments for acceptance. Acceptance shall demonstrate complete Report access and execution through the selected supported option.

*Priority rationale:* Client access is an explicitly stated deployment requirement, while the source wording permits either client environment.

#### CON-029 - Supported Server Platforms

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D10, D16, D18

The system shall be deployable and operational on both Linux, including Red Hat Enterprise Linux, and Solaris 10 on SPARC server environments. Deployment documentation shall identify the supported configurations for both operating-system families. Acceptance shall verify installation, startup, and Report execution on each required platform.

*Priority rationale:* The sources explicitly require both server operating-system families for primary and secondary deployment environments.

#### CON-030 - Use Enterprise ILS Data

**Priority:** Must &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D10, D18, D19

The system shall rely on and interoperate with the enterprise ILS data structures and supported functionality, including Acquisitions and Cataloging data. It shall read and query this data for management Reports and related operations. It shall not manage or modify Acquisitions or Cataloging functions.

*Priority rationale:* The system depends on the enterprise ILS as the authoritative source for core Acquisitions and Cataloging data.

#### CON-031 - Disaster Recovery Site Operation

**Priority:** Should &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D16

The system shall support operation at the secondary disaster recovery site running Solaris 10 on SPARC. Reporting and applicable recovery processes shall remain available when deployed at that site. Acceptance shall verify installation and execution at the secondary site using its available infrastructure.

*Priority rationale:* Secondary-site operation is important for resilience and recovery, although routine operations can continue at the primary site.

### 6.11 Record Purging

#### NFR-021 - Record Purge Audit Trail

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D06

The system shall record every purge action in an Audit Log. Each entry shall identify who performed the action, what records were purged, and when the action occurred. The recorded information shall support accountability and investigation of purge operations.

*Priority rationale:* Auditable deletion accountability is explicitly required for all purge actions and supports safe administration.

### 6.12 Report Operations

#### NFR-022 - Accurate Reliable Report Output

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D10

The system shall produce Report output that is accurate and reliable for stakeholder decision making. Report output shall be tested against appropriate source data and expected results before it is accepted for operational use. Test evidence shall demonstrate that the Report produces consistent results for defined test cases.

*Priority rationale:* Stakeholders must be able to trust Reports used for decisions, making output quality essential.

#### NFR-023 - Visible Report Criteria

**Priority:** Should &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D10

The system shall present the selection criteria applied to a Report clearly in the reporting interface. Users shall be able to identify the filters and parameters before executing the Report. The displayed criteria shall correspond to the criteria used for the generated results.

*Priority rationale:* Clear criteria visibility reduces reporting errors and is directly requested as a usability need.

### 6.13 Report Scheduling

#### NFR-024 - Asynchronous Report Processing

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D14, D16, D18

The system shall place long-running, complex, and scheduled Report requests in the Report Queue for background execution. Queue processing shall continue during open hours without blocking interactive use or materially slowing the Circulation client and other production workflows. Acceptance shall verify that a queued Report executes asynchronously, that queue status is maintained, and that representative interactive operations remain available during execution.

*Priority rationale:* Non-interfering background execution is essential for a shared reporting system operating during normal library hours.

### 6.14 Transit Monitoring

#### CON-032 - Transit Detection Logic

**Priority:** Should &nbsp;·&nbsp; **Type:** constraint &nbsp;·&nbsp; **Sources:** D05

The system shall identify an Item as overdue in Transit when its Transit record has no arrival date and its departure date is older than the configured Transit threshold. The detection shall use the applicable Transit data records as the source of departure and arrival information. Items meeting these conditions shall be eligible for the overdue Transit Report.

*Priority rationale:* The specified detection rule provides a concrete and consistent basis for overdue Transit reporting, although it is an implementation constraint rather than a user-facing core feature.

### 6.15 Uncataloged Materials

#### NFR-025 - Quick Uncataloged Item Distribution

**Priority:** Must &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D10, D15

The system shall support rapid distribution workflows for uncataloged Items, including Items received in large shipments. These workflows shall enable staff to process and assign Items for deployment with minimal delay. Acceptance requires that a representative batch of uncataloged Items can be distributed through the workflow without unnecessary per-Item processing steps.

*Priority rationale:* Rapid distribution is explicitly requested and is essential to handling incoming uncataloged shipments efficiently.

#### NFR-026 - Minimize Branch Labor

**Priority:** Should &nbsp;·&nbsp; **Type:** non-functional &nbsp;·&nbsp; **Sources:** D10, D15

The system shall provide uncataloged Item receiving, tracking, and distribution workflows that minimize Branch staff effort per Item. The workflows shall avoid unnecessary manual steps while preserving the information needed to account for and distribute the Items. Acceptance requires that staff can complete the defined workflow with low and measurable processing effort per Item.

*Priority rationale:* Reducing Branch labor is strongly requested and important for operational cost control, although a manual workaround remains possible.

## 7. Traceability

### 7.1 Requirement to sources

| Requirement | Name | Priority | Source documents |
|---|---|---|---|
| FR-001 | Staff Badge Authentication | Must | D10 (`early_draft_srs_galecia.txt`), D13 (`email_staff_login.eml`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| FR-002 | Staff Login Audit Logging | Must | D13 (`email_staff_login.eml`) |
| FR-003 | Unattended Session Protection | Must | D13 (`email_staff_login.eml`) |
| FR-004 | Quick Staff Session Switching | Should | D13 (`email_staff_login.eml`) |
| FR-005 | Bibliographic Fields For Reporting | Must | D14 (`evergreen_reference_2009.txt`) |
| FR-006 | Bibliographic Record Addition Report | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-007 | Bibliographic Record Count Report | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-008 | Bibliographic Record Edit Report | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-009 | Bibliographic Records Without Items | Must | D10 (`early_draft_srs_galecia.txt`) |
| FR-010 | Catalog Data Quality Reports | Must | D15 (`interview_cataloging_2009-05-08.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| FR-011 | Missing MARC Field Report | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-012 | Reportable Data Relationships | Must | D14 (`evergreen_reference_2009.txt`) |
| FR-013 | Reportable Record Types | Must | D14 (`evergreen_reference_2009.txt`) |
| FR-014 | Circulation Canned Reports | Should | D14 (`evergreen_reference_2009.txt`) |
| FR-015 | Monthly Patron Addition Report | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-016 | Patron Canned Reports | Should | D14 (`evergreen_reference_2009.txt`) |
| FR-017 | Checkin Count Report | Must | D10 (`early_draft_srs_galecia.txt`) |
| FR-018 | Checkin Method Counts | Must | D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`) |
| FR-019 | Checkout Count Report | Must | D10 (`early_draft_srs_galecia.txt`) |
| FR-020 | Checkout Type Counts | Must | D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`) |
| FR-021 | Circulation Counts By Type | Must | D10 (`early_draft_srs_galecia.txt`) |
| FR-022 | Core Circulation Activity Metrics | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`) |
| FR-023 | Distinct Checkin Timestamp | Must | D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`) |
| FR-024 | Multi Scope Transaction Aggregates | Must | D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`) |
| FR-025 | Overdue Item Reports | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-026 | Renewals Count Report | Must | D10 (`early_draft_srs_galecia.txt`) |
| FR-027 | Circulation By Patron County | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-028 | Circulation By Patron Home Branch | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-029 | Circulation Counts By Dewey | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-030 | Circulation Counts By MARC | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-031 | Circulation Counts By Shelf Location | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-032 | Circulation Modifier Category Counts | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-033 | Claims Returned Report | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-034 | Date-Based Item Use Counts | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-035 | Hold Placement Methods | Should | D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`) |
| FR-036 | Include Uncataloged Circulation | Should | D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-037 | Item Use Count Filtering | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-038 | Last Circulation Date | Should | D14 (`evergreen_reference_2009.txt`) |
| FR-039 | Transaction Dimension Grouping | Should | D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`) |
| FR-040 | Items By Fines Stopped Reason | Could | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-041 | All Branch Capacity Overview | Must | D02 (`conversations/conv_pines015_capacity_interface.eml`), D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| FR-042 | Break Down Collection Categories | Must | D01 (`conversations/conv_pines014_material_volume.eml`), D03 (`conversations/conv_pines016_shelf_space.eml`) |
| FR-043 | Cross-Branch Capacity Access | Must | D02 (`conversations/conv_pines015_capacity_interface.eml`) |
| FR-044 | Define Capacity Metrics | Must | D02 (`conversations/conv_pines015_capacity_interface.eml`) |
| FR-045 | Drill Into Branch Capacity | Must | D01 (`conversations/conv_pines014_material_volume.eml`), D02 (`conversations/conv_pines015_capacity_interface.eml`) |
| FR-046 | Estimate Shelf Space | Must | D03 (`conversations/conv_pines016_shelf_space.eml`) |
| FR-047 | Material Volume Report | Must | D01 (`conversations/conv_pines014_material_volume.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-048 | Shelf Space Comparison Report | Must | D03 (`conversations/conv_pines016_shelf_space.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| FR-049 | Branch Comparison View | Should | D03 (`conversations/conv_pines016_shelf_space.eml`) |
| FR-050 | Capacity Trend Reporting | Should | D02 (`conversations/conv_pines015_capacity_interface.eml`) |
| FR-051 | Collection Volume Trend Reporting | Should | D01 (`conversations/conv_pines014_material_volume.eml`) |
| FR-052 | Compare Branch Capacity | Should | D03 (`conversations/conv_pines016_shelf_space.eml`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| FR-053 | Configurable Aggregation Levels | Should | D03 (`conversations/conv_pines016_shelf_space.eml`), D09 (`conversations/conv_pines024_inactive_patrons.eml`) |
| FR-054 | Consolidated Volume Report | Should | D01 (`conversations/conv_pines014_material_volume.eml`) |
| FR-055 | Export Capacity Data | Should | D02 (`conversations/conv_pines015_capacity_interface.eml`), D03 (`conversations/conv_pines016_shelf_space.eml`) |
| FR-056 | Filter Acquisition Date Ranges | Should | D01 (`conversations/conv_pines014_material_volume.eml`) |
| FR-057 | Filter Branch Capacity | Should | D02 (`conversations/conv_pines015_capacity_interface.eml`) |
| FR-058 | Filter Reports By Date | Should | D03 (`conversations/conv_pines016_shelf_space.eml`) |
| FR-059 | Group Branch Capacity | Should | D02 (`conversations/conv_pines015_capacity_interface.eml`) |
| FR-060 | Report Holds By Category | Should | D01 (`conversations/conv_pines014_material_volume.eml`) |
| FR-061 | Show Historical Volume | Should | D01 (`conversations/conv_pines014_material_volume.eml`) |
| FR-062 | Sortable Capacity Results | Should | D02 (`conversations/conv_pines015_capacity_interface.eml`) |
| FR-063 | Color-Coded Capacity Indicators | Could | D02 (`conversations/conv_pines015_capacity_interface.eml`) |
| FR-064 | Customizable Volume Categories | Could | D01 (`conversations/conv_pines014_material_volume.eml`) |
| FR-065 | List Checked-Out Items | Could | D10 (`early_draft_srs_galecia.txt`) |
| FR-066 | Aggregate Deletion Counts | Must | D07 (`conversations/conv_pines022_deletions.eml`), D10 (`early_draft_srs_galecia.txt`) |
| FR-067 | Capture Deletion Audit Events | Must | D07 (`conversations/conv_pines022_deletions.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`), D20 (`survey_results_2009.txt`) |
| FR-068 | Query Deleted Record Audit | Must | D07 (`conversations/conv_pines022_deletions.eml`) |
| FR-069 | Filter Transaction Audit Reports | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-070 | Log Denied Deletion Attempts | Should | D07 (`conversations/conv_pines022_deletions.eml`) |
| FR-071 | Rank Deleting Staff | Could | D07 (`conversations/conv_pines022_deletions.eml`) |
| FR-072 | Integrated Searchable Help | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| FR-073 | Administrative Error Feedback | Should | D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| FR-074 | Associate Financial Transactions | Must | D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`) |
| FR-075 | Core Financial Reports | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-076 | Maintain Payment Ledger | Must | D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`) |
| FR-077 | Query High-Balance Accounts | Must | D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`) |
| FR-078 | Report Fines By Period | Must | D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`) |
| FR-079 | Report Patron Account Balances | Must | D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`) |
| FR-080 | Report Payments By Method | Must | D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`) |
| FR-081 | Track Financial Transactions | Must | D10 (`early_draft_srs_galecia.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`) |
| FR-082 | Join Financial Data Sources | Should | D11 (`email_financial_reports.eml`) |
| FR-083 | Provide Director Financial Reporting | Should | D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| FR-084 | Report Historical Bill Snapshots | Should | D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`) |
| FR-085 | Report Item Monetary Values | Should | D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`), D14 (`evergreen_reference_2009.txt`) |
| FR-086 | Report Voided Transactions | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-087 | Report Waived Fines | Should | D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`) |
| FR-088 | Report Alternative Payments | Could | D10 (`early_draft_srs_galecia.txt`) |
| FR-089 | Stale Holds Report | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-090 | Unfilled Holds Report | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-091 | Annual Holds Placed Count | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-092 | Bibliographic Records With Holds | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-093 | Holds Purchase Alert | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-094 | IntraPINES Loan Reporting | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-095 | Item-Level Holds Report | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-096 | Items Received For Holds | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-097 | Items Sent For Holds | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-098 | Items Without Recent Checkouts | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-099 | Missing Items Report | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-100 | Item Activity Reports | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-101 | Periodic Last Item Report | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-102 | Standard Item Canned Reports | Must | D14 (`evergreen_reference_2009.txt`) |
| FR-103 | Weeding Reports With Use History | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D20 (`survey_results_2009.txt`) |
| FR-104 | Collection Age By Location | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-105 | Configurable Weeding Criteria | Should | D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-106 | Item Last Edit Date | Should | D14 (`evergreen_reference_2009.txt`), D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-107 | Items By Bibliographic Content | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-108 | Items By Creation Date | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-109 | Low Use Weeding Report | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-110 | Missing Item Report | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-111 | Periodic Invalid Item Reports | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-112 | Invalid Patron Home Branch Report | Could | D10 (`early_draft_srs_galecia.txt`) |
| FR-113 | Missing Patterns By Shelf | Could | D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-114 | Periodic Long Call Number Reports | Could | D10 (`early_draft_srs_galecia.txt`) |
| FR-115 | Batch Item Transfer Utility | Must | D04 (`conversations/conv_pines018_item_transfer.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-116 | Manually Select Transfer Items | Must | D04 (`conversations/conv_pines018_item_transfer.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`), D20 (`survey_results_2009.txt`) |
| FR-117 | Protect Checked-Out Items | Must | D04 (`conversations/conv_pines018_item_transfer.eml`) |
| FR-118 | Query Transfer Candidates | Must | D04 (`conversations/conv_pines018_item_transfer.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`), D20 (`survey_results_2009.txt`) |
| FR-119 | Restrict Transfer Permissions | Must | D04 (`conversations/conv_pines018_item_transfer.eml`) |
| FR-120 | Time-Based Item Reversion | Must | D04 (`conversations/conv_pines018_item_transfer.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-121 | Update Item Locations | Must | D04 (`conversations/conv_pines018_item_transfer.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`), D20 (`survey_results_2009.txt`) |
| FR-122 | Criteria-Based Item Reversion | Should | D04 (`conversations/conv_pines018_item_transfer.eml`) |
| FR-123 | Generate Transfer Pull Lists | Should | D04 (`conversations/conv_pines018_item_transfer.eml`), D10 (`early_draft_srs_galecia.txt`) |
| FR-124 | Manage Temporary Locations | Should | D04 (`conversations/conv_pines018_item_transfer.eml`) |
| FR-125 | Preview And Confirm Transfers | Should | D04 (`conversations/conv_pines018_item_transfer.eml`) |
| FR-126 | Print Transit Labels | Should | D04 (`conversations/conv_pines018_item_transfer.eml`) |
| FR-127 | Schedule Reversion Processing | Should | D04 (`conversations/conv_pines018_item_transfer.eml`) |
| FR-128 | Track Item Transfer History | Should | D04 (`conversations/conv_pines018_item_transfer.eml`) |
| FR-129 | Undo Transfer Operations | Should | D04 (`conversations/conv_pines018_item_transfer.eml`), D20 (`survey_results_2009.txt`) |
| FR-130 | Alert On Transfer Issues | Could | D04 (`conversations/conv_pines018_item_transfer.eml`) |
| FR-131 | Branch Capacity Analysis | Must | D10 (`early_draft_srs_galecia.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`) |
| FR-132 | Collection Use Analysis | Must | D10 (`early_draft_srs_galecia.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`) |
| FR-133 | Manager Planning Reports | Must | D10 (`early_draft_srs_galecia.txt`) |
| FR-134 | Staff Productivity Analysis | Must | D10 (`early_draft_srs_galecia.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`), D20 (`survey_results_2009.txt`) |
| FR-135 | Collection Development Reports | Should | D20 (`survey_results_2009.txt`) |
| FR-136 | Executive Strategic Reports | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-137 | Program Attendance Reports | Should | D20 (`survey_results_2009.txt`) |
| FR-138 | Geographic Age Demographics | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D20 (`survey_results_2009.txt`) |
| FR-139 | Geographic Patron Counts | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-140 | Patron Characteristic Reporting | Must | D08 (`conversations/conv_pines023_patron_characteristics.eml`), D10 (`early_draft_srs_galecia.txt`) |
| FR-141 | Patron Demographic Planning | Must | D10 (`early_draft_srs_galecia.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| FR-142 | Reportable Patron Fields | Must | D14 (`evergreen_reference_2009.txt`) |
| FR-143 | Total Patron Count | Must | D10 (`early_draft_srs_galecia.txt`) |
| FR-144 | Circulation By Patron Age | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-145 | Filter By Survey Name | Should | D10 (`early_draft_srs_galecia.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| FR-146 | List Barred Patrons | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-147 | New Patron Demographic Counts | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-148 | Patron Behavior Analytics | Should | D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`) |
| FR-149 | Patron Count By Branch | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-150 | Patron Count By Profile | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-151 | Patron Lists By Expiration | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-152 | Patron Reports By Survey Answer | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-153 | Staff Password Audit Report | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-154 | Patron Lists By Note Text | Could | D10 (`early_draft_srs_galecia.txt`) |
| FR-155 | Voter Registration Counts | Could | D10 (`early_draft_srs_galecia.txt`) |
| FR-156 | Voter Responses By County Week | Could | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-157 | Configurable Inactivity Thresholds | Must | D09 (`conversations/conv_pines024_inactive_patrons.eml`) |
| FR-158 | Inactive Patron Exclusions | Must | D09 (`conversations/conv_pines024_inactive_patrons.eml`) |
| FR-159 | Inactive Patron Report | Must | D08 (`conversations/conv_pines023_patron_characteristics.eml`), D09 (`conversations/conv_pines024_inactive_patrons.eml`), D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-160 | Aggregated Patron Metrics | Should | D08 (`conversations/conv_pines023_patron_characteristics.eml`) |
| FR-161 | Branch Cleanup Assignment | Should | D09 (`conversations/conv_pines024_inactive_patrons.eml`) |
| FR-162 | Configurable Age Brackets | Should | D08 (`conversations/conv_pines023_patron_characteristics.eml`) |
| FR-163 | Inactive Patron Mailing Addresses | Should | D09 (`conversations/conv_pines024_inactive_patrons.eml`) |
| FR-164 | Inactive Patrons By Branch | Should | D09 (`conversations/conv_pines024_inactive_patrons.eml`) |
| FR-165 | Incomplete Patron Data Handling | Should | D08 (`conversations/conv_pines023_patron_characteristics.eml`) |
| FR-166 | Logical Filter Combination | Should | D08 (`conversations/conv_pines023_patron_characteristics.eml`) |
| FR-167 | Outstanding Fine Flag | Should | D09 (`conversations/conv_pines024_inactive_patrons.eml`) |
| FR-168 | Scheduled Inactivity Reports | Should | D09 (`conversations/conv_pines024_inactive_patrons.eml`) |
| FR-169 | Centralized Multi-Branch Operations | Must | D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| FR-170 | Protect Deleted Item Visibility | Must | D10 (`early_draft_srs_galecia.txt`) |
| FR-171 | Query OPAC Activity Data | Must | D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| FR-172 | WorldCat Integration Support | Must | D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-173 | Historical Data Reporting | Should | D20 (`survey_results_2009.txt`) |
| FR-174 | Historical Reporting Warehouse | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| FR-175 | Integrate Vendor Data | Should | D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| FR-176 | Local Administrative Configuration | Should | D10 (`early_draft_srs_galecia.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`) |
| FR-177 | Migrate Environment Configuration | Should | D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| FR-178 | Reports For Notices Sent | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-179 | Batch Item Status Conversion | Must | D06 (`conversations/conv_pines021_item_purging.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-180 | Controlled Purge Execution | Must | D06 (`conversations/conv_pines021_item_purging.eml`) |
| FR-181 | Identify Purge Candidates | Must | D06 (`conversations/conv_pines021_item_purging.eml`), D10 (`early_draft_srs_galecia.txt`) |
| FR-182 | Purge Volumes And Orphans | Must | D06 (`conversations/conv_pines021_item_purging.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-183 | Sole Item Purge Flagging | Must | D06 (`conversations/conv_pines021_item_purging.eml`) |
| FR-184 | Report Deleted Sole Copies | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-185 | Schedule Purge Operations | Should | D06 (`conversations/conv_pines021_item_purging.eml`) |
| FR-186 | Boolean Query Logic | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`) |
| FR-187 | Controlled Template Editing | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`) |
| FR-188 | Display Query Criteria | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`) |
| FR-189 | Field Selection And Filtering | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`) |
| FR-190 | Interactive Report Authoring | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`), D20 (`survey_results_2009.txt`) |
| FR-191 | Report Template Management | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| FR-192 | Run Or Modify Templates | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D20 (`survey_results_2009.txt`) |
| FR-193 | Support Specified Report Definitions | Must | D10 (`early_draft_srs_galecia.txt`) |
| FR-194 | Clone Report Definitions | Should | D12 (`email_report_features.eml`) |
| FR-195 | Cross-Tabulation And Pivoting | Should | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`) |
| FR-196 | Edit Canned Report Displays | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-197 | Picklist Query Values | Should | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`) |
| FR-198 | Regular Expression Queries | Should | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`) |
| FR-199 | Reusable Report And Query Definitions | Should | D04 (`conversations/conv_pines018_item_transfer.eml`), D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D15 (`interview_cataloging_2009-05-08.txt`), D20 (`survey_results_2009.txt`) |
| FR-200 | Explicit Null And Blank Values | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`), D20 (`survey_results_2009.txt`) |
| FR-201 | Multiple Report Export Formats | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`), D20 (`survey_results_2009.txt`) |
| FR-202 | Email Report Results | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`) |
| FR-203 | MARC Values Per Record | Should | D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`) |
| FR-204 | Text File Report Filtering | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-205 | Deduplicated Excel Results | Could | D20 (`survey_results_2009.txt`) |
| FR-206 | Predefined Board Executive Reports | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| FR-207 | Systemwide Statistical Reports | Must | D10 (`early_draft_srs_galecia.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`) |
| FR-208 | Three Reporting Interfaces | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-209 | Comparative Period Columns | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-210 | Executive Reports Interface | Should | D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| FR-211 | Management Reporting Tools | Should | D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`) |
| FR-212 | On-Demand Report Criteria | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-213 | Open Template Reporting | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-214 | Report Quick Access Descriptions | Should | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-215 | Report Result Identification | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-216 | Selectable Report Data | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-217 | Current Data Reporting | Could | D10 (`early_draft_srs_galecia.txt`) |
| FR-218 | Ad Hoc Data Access Control | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`) |
| FR-219 | Destructive Operation Permissions | Must | D06 (`conversations/conv_pines021_item_purging.eml`) |
| FR-220 | Fine-Grained Report Permissions | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`) |
| FR-221 | Predefined Report Roles | Must | D10 (`early_draft_srs_galecia.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| FR-222 | Role Assignment Administration | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D13 (`email_staff_login.eml`), D16 (`interview_sysadmin_2009-05-10.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| FR-223 | Role-Based Access Control | Must | D10 (`early_draft_srs_galecia.txt`), D13 (`email_staff_login.eml`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| FR-224 | Table And Field Access | Must | D10 (`early_draft_srs_galecia.txt`) |
| FR-225 | Permission-Based Filter Restrictions | Should | D14 (`evergreen_reference_2009.txt`) |
| FR-226 | Shared Report Folders | Should | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`) |
| FR-227 | Cancel Report Execution | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`), D20 (`survey_results_2009.txt`) |
| FR-228 | Flexible Report Scheduling | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`) |
| FR-229 | Prioritize And Preempt Reports | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`) |
| FR-230 | Report Queue Visibility | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D20 (`survey_results_2009.txt`) |
| FR-231 | Edit Recurring Report Schedules | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-232 | Batch Report Execution | Could | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-233 | Canned Report Scheduling Interface | Could | D10 (`early_draft_srs_galecia.txt`) |
| FR-234 | Relative Date Report Execution | Could | D10 (`early_draft_srs_galecia.txt`) |
| FR-235 | Report Delivery Address Book | Could | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`) |
| FR-236 | Branch Missing Damage Reports | Must | D05 (`conversations/conv_pines019_020_missing_intransit.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| FR-237 | Combined Transit Direction Report | Must | D05 (`conversations/conv_pines019_020_missing_intransit.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-238 | Missing Damage Counts | Must | D05 (`conversations/conv_pines019_020_missing_intransit.eml`) |
| FR-239 | Periodic Overdue Transit Reports | Must | D05 (`conversations/conv_pines019_020_missing_intransit.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-240 | Transit Reports By Branches | Must | D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| FR-241 | Exportable Operational Reports | Should | D05 (`conversations/conv_pines019_020_missing_intransit.eml`) |
| FR-242 | Filter By Item Status | Should | D05 (`conversations/conv_pines019_020_missing_intransit.eml`) |
| FR-243 | Item Condition Notes | Should | D05 (`conversations/conv_pines019_020_missing_intransit.eml`) |
| FR-244 | Missing Damage Date Filters | Should | D05 (`conversations/conv_pines019_020_missing_intransit.eml`) |
| FR-245 | Reports By Bibliographic Record | Should | D05 (`conversations/conv_pines019_020_missing_intransit.eml`) |
| FR-246 | Sort Transit Items By Due Date | Should | D05 (`conversations/conv_pines019_020_missing_intransit.eml`) |
| FR-247 | Transit Items With Holds | Should | D10 (`early_draft_srs_galecia.txt`) |
| FR-248 | Uncataloged Item Inventory | Must | D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-249 | Report Uncataloged Item Use | Should | D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`) |
| FR-250 | Report Cataloged In-House Use | Could | D10 (`early_draft_srs_galecia.txt`) |
| NFR-001 | At-A-Glance Capacity Decisions | Should | D02 (`conversations/conv_pines015_capacity_interface.eml`) |
| NFR-002 | Large Location Usability | Should | D02 (`conversations/conv_pines015_capacity_interface.eml`) |
| NFR-003 | Outlier Identification Presentation | Should | D03 (`conversations/conv_pines016_shelf_space.eml`) |
| NFR-004 | Retain Deletion Audit Logs | Must | D07 (`conversations/conv_pines022_deletions.eml`) |
| NFR-005 | Accessible User Interfaces | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| NFR-006 | Protect Archived Financial Privacy | Must | D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`) |
| NFR-007 | Update Payments Immediately | Must | D11 (`email_financial_reports.eml`) |
| NFR-008 | Edit Financial Information | Should | D10 (`early_draft_srs_galecia.txt`) |
| NFR-009 | Consortium Scale Support | Must | D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| NFR-010 | Ensure Transaction-Safe Updates | Must | D04 (`conversations/conv_pines018_item_transfer.eml`) |
| NFR-011 | Log Transfer Operations | Must | D04 (`conversations/conv_pines018_item_transfer.eml`) |
| NFR-012 | Scale Large Transfer Updates | Must | D04 (`conversations/conv_pines018_item_transfer.eml`) |
| NFR-013 | Anonymized Demographic Reporting | Must | D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`) |
| NFR-014 | Large Patron Dataset Performance | Must | D09 (`conversations/conv_pines024_inactive_patrons.eml`) |
| NFR-015 | Background Inactivity Processing | Should | D09 (`conversations/conv_pines024_inactive_patrons.eml`) |
| NFR-016 | Non Disruptive Reporting | Must | D10 (`early_draft_srs_galecia.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| NFR-017 | Training Data Isolation | Must | D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| NFR-018 | Discoverable Reports Interface | Should | D20 (`survey_results_2009.txt`) |
| NFR-019 | Real-Time Reporting Capability | Should | D20 (`survey_results_2009.txt`) |
| NFR-020 | Report Performance Under Load | Should | D20 (`survey_results_2009.txt`) |
| NFR-021 | Record Purge Audit Trail | Must | D06 (`conversations/conv_pines021_item_purging.eml`) |
| NFR-022 | Accurate Reliable Report Output | Must | D10 (`early_draft_srs_galecia.txt`) |
| NFR-023 | Visible Report Criteria | Should | D10 (`early_draft_srs_galecia.txt`) |
| NFR-024 | Asynchronous Report Processing | Must | D14 (`evergreen_reference_2009.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| NFR-025 | Quick Uncataloged Item Distribution | Must | D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`) |
| NFR-026 | Minimize Branch Labor | Should | D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`) |
| CON-001 | Optional Card Reader Support | Must | D13 (`email_staff_login.eml`) |
| CON-002 | Use Acquisition Dates | Must | D01 (`conversations/conv_pines014_material_volume.eml`) |
| CON-003 | Persist Deletion Audit Records | Must | D07 (`conversations/conv_pines022_deletions.eml`) |
| CON-004 | Adapted Requirements Foundation | Must | D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`) |
| CON-005 | Complete Data Specifications | Must | D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| CON-006 | High-Level Process Documentation | Should | D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| CON-007 | Readable Requirements Specification | Should | D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`) |
| CON-008 | Library Terminology Assumption | Could | D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`) |
| CON-009 | Defer Detailed Interface Specification | Won't | D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`) |
| CON-010 | Meet Financial Audit Requirements | Must | D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`) |
| CON-011 | Retain Financial Transaction History | Must | D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`), D12 (`email_report_features.eml`), D20 (`survey_results_2009.txt`) |
| CON-012 | Reuse Existing Query Builder | Should | D04 (`conversations/conv_pines018_item_transfer.eml`) |
| CON-013 | Supported Web Browsers | Should | D10 (`early_draft_srs_galecia.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| CON-014 | Qualifying Activity Calculation | Must | D09 (`conversations/conv_pines024_inactive_patrons.eml`) |
| CON-015 | Calculate Age From Birthdate | Should | D08 (`conversations/conv_pines023_patron_characteristics.eml`) |
| CON-016 | CSV Report Export | Should | D09 (`conversations/conv_pines024_inactive_patrons.eml`) |
| CON-017 | Enterprise Infrastructure Compatibility | Must | D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| CON-018 | Enterprise Library System Integration | Must | D10 (`early_draft_srs_galecia.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| CON-019 | Normalized Relational Reporting | Must | D16 (`interview_sysadmin_2009-05-10.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| CON-020 | Patron-Facing Scope Boundary | Must | D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`) |
| CON-021 | PostgreSQL Platform Compatibility | Must | D16 (`interview_sysadmin_2009-05-10.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| CON-022 | Preserve OPAC Independence | Must | D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| CON-023 | Production Reporting Isolation | Must | D14 (`evergreen_reference_2009.txt`), D16 (`interview_sysadmin_2009-05-10.txt`) |
| CON-024 | Relational Database Backend | Must | D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| CON-025 | Run On Existing Hardware | Must | D16 (`interview_sysadmin_2009-05-10.txt`) |
| CON-026 | Separated Development Training Environments | Must | D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| CON-027 | Standards-Compliant HTML Output | Must | D10 (`early_draft_srs_galecia.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| CON-028 | Supported Client Access | Must | D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| CON-029 | Supported Server Platforms | Must | D10 (`early_draft_srs_galecia.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`) |
| CON-030 | Use Enterprise ILS Data | Must | D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`) |
| CON-031 | Disaster Recovery Site Operation | Should | D16 (`interview_sysadmin_2009-05-10.txt`) |
| CON-032 | Transit Detection Logic | Should | D05 (`conversations/conv_pines019_020_missing_intransit.eml`) |

### 7.2 Source to requirements

| Document | Requirements derived | Blacklisted |
|---|---|---|
| D01 `conversations/conv_pines014_material_volume.eml` | FR-042, FR-045, FR-047, FR-051, FR-054, FR-056, FR-060, FR-061, FR-064, CON-002 | - |
| D02 `conversations/conv_pines015_capacity_interface.eml` | FR-041, FR-043, FR-044, FR-045, FR-050, FR-055, FR-057, FR-059, FR-062, FR-063, NFR-001, NFR-002 | BL-001, BL-002 |
| D03 `conversations/conv_pines016_shelf_space.eml` | FR-042, FR-046, FR-048, FR-049, FR-052, FR-053, FR-055, FR-058, NFR-003 | - |
| D04 `conversations/conv_pines018_item_transfer.eml` | FR-115, FR-116, FR-117, FR-118, FR-119, FR-120, FR-121, FR-122, FR-123, FR-124, FR-125, FR-126, FR-127, FR-128, FR-129, FR-130, FR-199, NFR-010, NFR-011, NFR-012, CON-012 | BL-003 |
| D05 `conversations/conv_pines019_020_missing_intransit.eml` | FR-236, FR-237, FR-238, FR-239, FR-241, FR-242, FR-243, FR-244, FR-245, FR-246, CON-032 | - |
| D06 `conversations/conv_pines021_item_purging.eml` | FR-179, FR-180, FR-181, FR-182, FR-183, FR-185, FR-219, NFR-021 | - |
| D07 `conversations/conv_pines022_deletions.eml` | FR-066, FR-067, FR-068, FR-070, FR-071, NFR-004, CON-003 | - |
| D08 `conversations/conv_pines023_patron_characteristics.eml` | FR-140, FR-159, FR-160, FR-162, FR-165, FR-166, CON-015 | - |
| D09 `conversations/conv_pines024_inactive_patrons.eml` | FR-053, FR-157, FR-158, FR-159, FR-161, FR-163, FR-164, FR-167, FR-168, NFR-014, NFR-015, CON-014, CON-016 | - |
| D10 `early_draft_srs_galecia.txt` | FR-001, FR-006, FR-007, FR-008, FR-009, FR-011, FR-015, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022, FR-024, FR-025, FR-026, FR-027, FR-028, FR-029, FR-030, FR-031, FR-032, FR-033, FR-034, FR-035, FR-036, FR-037, FR-039, FR-040, FR-041, FR-047, FR-048, FR-065, FR-066, FR-067, FR-069, FR-072, FR-073, FR-074, FR-075, FR-076, FR-077, FR-078, FR-079, FR-080, FR-081, FR-085, FR-086, FR-087, FR-088, FR-089, FR-090, FR-091, FR-092, FR-093, FR-094, FR-095, FR-096, FR-097, FR-098, FR-099, FR-100, FR-101, FR-103, FR-104, FR-107, FR-108, FR-109, FR-110, FR-111, FR-112, FR-114, FR-115, FR-116, FR-118, FR-120, FR-121, FR-123, FR-131, FR-132, FR-133, FR-134, FR-136, FR-138, FR-139, FR-140, FR-141, FR-143, FR-144, FR-145, FR-146, FR-147, FR-148, FR-149, FR-150, FR-151, FR-152, FR-153, FR-154, FR-155, FR-156, FR-159, FR-169, FR-170, FR-171, FR-174, FR-175, FR-176, FR-178, FR-179, FR-181, FR-182, FR-184, FR-186, FR-187, FR-188, FR-189, FR-190, FR-191, FR-192, FR-193, FR-195, FR-196, FR-197, FR-198, FR-199, FR-200, FR-201, FR-202, FR-203, FR-204, FR-206, FR-207, FR-208, FR-209, FR-212, FR-213, FR-214, FR-215, FR-216, FR-217, FR-218, FR-220, FR-221, FR-222, FR-223, FR-224, FR-226, FR-227, FR-228, FR-229, FR-230, FR-231, FR-232, FR-233, FR-234, FR-235, FR-236, FR-237, FR-239, FR-240, FR-247, FR-248, FR-249, FR-250, NFR-005, NFR-006, NFR-008, NFR-009, NFR-013, NFR-016, NFR-022, NFR-023, NFR-025, NFR-026, CON-005, CON-006, CON-010, CON-011, CON-013, CON-018, CON-022, CON-024, CON-026, CON-027, CON-028, CON-029, CON-030 | - |
| D11 `email_financial_reports.eml` | FR-074, FR-076, FR-077, FR-078, FR-079, FR-080, FR-082, FR-085, FR-087, NFR-007, CON-010, CON-011 | - |
| D12 `email_report_features.eml` | FR-022, FR-138, FR-186, FR-187, FR-188, FR-189, FR-190, FR-191, FR-192, FR-194, FR-195, FR-197, FR-198, FR-206, FR-218, FR-220, FR-222, FR-226, FR-229, FR-230, NFR-006, CON-011 | - |
| D13 `email_staff_login.eml` | FR-001, FR-002, FR-003, FR-004, FR-222, FR-223, CON-001 | BL-007, BL-013 |
| D14 `evergreen_reference_2009.txt` | FR-005, FR-006, FR-007, FR-008, FR-011, FR-012, FR-013, FR-014, FR-016, FR-023, FR-025, FR-027, FR-029, FR-030, FR-032, FR-033, FR-037, FR-038, FR-040, FR-072, FR-075, FR-084, FR-085, FR-089, FR-090, FR-093, FR-100, FR-101, FR-102, FR-103, FR-104, FR-106, FR-108, FR-139, FR-142, FR-144, FR-153, FR-156, FR-159, FR-174, FR-186, FR-188, FR-189, FR-190, FR-191, FR-195, FR-196, FR-198, FR-199, FR-200, FR-201, FR-202, FR-204, FR-208, FR-213, FR-214, FR-220, FR-225, FR-226, FR-227, FR-228, FR-229, FR-230, FR-232, FR-235, NFR-005, NFR-024, CON-023, CON-026 | BL-010, BL-011 |
| D15 `interview_cataloging_2009-05-08.txt` | FR-010, FR-036, FR-047, FR-048, FR-067, FR-101, FR-105, FR-106, FR-113, FR-115, FR-116, FR-118, FR-120, FR-121, FR-172, FR-179, FR-182, FR-199, FR-236, FR-237, FR-239, FR-248, FR-249, NFR-025, NFR-026 | BL-004 |
| D16 `interview_sysadmin_2009-05-10.txt` | FR-072, FR-222, FR-223, NFR-005, NFR-016, NFR-024, CON-013, CON-019, CON-021, CON-023, CON-025, CON-026, CON-027, CON-029, CON-031 | - |
| D17 `meeting_minutes/meeting_2009-03-15_minutes.txt` | FR-081, FR-131, FR-132, FR-134, FR-141, FR-176, FR-190, FR-191, FR-207, FR-210, FR-211, FR-221, CON-004, CON-007, CON-008, CON-009, CON-018, CON-020 | BL-005, BL-006, BL-008, BL-009, BL-012 |
| D18 `meeting_minutes/meeting_2009-07-20_minutes.txt` | FR-001, FR-010, FR-041, FR-048, FR-052, FR-072, FR-073, FR-083, FR-103, FR-141, FR-169, FR-171, FR-175, FR-191, FR-206, FR-210, FR-223, FR-230, FR-236, FR-240, NFR-005, NFR-009, NFR-024, CON-005, CON-006, CON-013, CON-018, CON-022, CON-024, CON-026, CON-027, CON-028, CON-029, CON-030 | BL-005 |
| D19 `meeting_tech_subcommittee_2009-06-30.txt` | FR-072, FR-073, FR-145, FR-169, FR-171, FR-174, FR-175, FR-177, FR-200, FR-201, FR-221, FR-222, FR-223, FR-227, NFR-005, NFR-016, NFR-017, CON-005, CON-006, CON-017, CON-019, CON-021, CON-022, CON-024, CON-026, CON-027, CON-030 | - |
| D20 `survey_results_2009.txt` | FR-018, FR-020, FR-023, FR-024, FR-035, FR-039, FR-067, FR-084, FR-103, FR-116, FR-118, FR-121, FR-129, FR-134, FR-135, FR-137, FR-138, FR-148, FR-173, FR-189, FR-190, FR-192, FR-195, FR-199, FR-200, FR-201, FR-202, FR-203, FR-205, FR-220, FR-226, FR-227, FR-228, FR-230, NFR-013, NFR-018, NFR-019, NFR-020, CON-011 | - |

## 8. Blacklist (discarded statements)

#### BL-001 - Investigate Technical Constraints

**Reason:** out of scope &nbsp;·&nbsp; **Sources:** D02

*Statement:* A technical investigation must be performed to identify feasibility constraints before building the interface.

*Why discarded:* This is a project activity rather than behavior required of the software. The resulting technical constraints may inform requirements, but conducting the investigation is not itself a system requirement.

#### BL-002 - Produce Initial Mockups

**Reason:** out of scope &nbsp;·&nbsp; **Sources:** D02

*Statement:* Initial mockups or visual designs of the capacity interface must be produced as project deliverables.

*Why discarded:* Producing initial mockups is a design and project deliverable, not a required runtime capability of the software. Interface behavior is captured by the retained Branch capacity requirements.

#### BL-003 - Careful Technical Design Required

**Reason:** out of scope &nbsp;·&nbsp; **Sources:** D04

*Statement:* The transfer utility requires careful system design and technical investigation.

*Why discarded:* This candidate describes a project planning or engineering activity rather than observable software behavior or a testable system constraint. Its concerns are addressed by the functional and scalability requirements instead.

#### BL-004 - Support Extensive Batch Operations

**Reason:** nonsensical &nbsp;·&nbsp; **Sources:** D15

*Statement:* The system must support extensive batch operations across cataloging functions, including queries, transfers, status changes, and deletions.

*Why discarded:* The statement is not measurable and bundles several distinct capabilities, including transfers and queries, without defining the required operations, limits, or acceptance criteria. Its purge-related portions are covered by the specific batch requirements.

#### BL-005 - Reports Testing Group Workflow

**Reason:** out of scope &nbsp;·&nbsp; **Sources:** D17, D18

*Statement:* All new Reports development shall be filtered through the Reports testing group before wider deployment.

*Why discarded:* These candidates specify a project or release-governance process rather than behavior required of the Report software. The process may be documented elsewhere, but it is not a Report Operations system requirement.

#### BL-006 - Requirement Gathering Interviews

**Reason:** out of scope &nbsp;·&nbsp; **Sources:** D17

*Statement:* Each working group member shall conduct an interview with staff at their library system to gather Report needs by a specified date.

*Why discarded:* This is a project action and meeting follow-up, not a requirement on the software. The interview deadline and participant obligations belong in project planning documentation.

#### BL-007 - Streamlined Login Improves Security

**Reason:** nonsensical &nbsp;·&nbsp; **Sources:** D13

*Statement:* The streamlined login method should improve security compared to manual credential entry by reducing password sharing and unattended logged-in terminals.

*Why discarded:* The candidate states an unmeasurable comparative outcome without defining a security metric, threat model, or acceptance threshold. The concrete security controls are captured by the requirements for individual card authentication, login auditing, and unattended session protection.

#### BL-008 - Architectural Constraints Meeting

**Reason:** out of scope &nbsp;·&nbsp; **Sources:** D17

*Statement:* A technical subcommittee must meet to identify and discuss architectural constraints affecting the reporting system.

*Why discarded:* This candidate specifies a meeting and project activity rather than behavior, quality, or constraint of the software.

#### BL-009 - Iterative Prototype Development

**Reason:** out of scope &nbsp;·&nbsp; **Sources:** D17

*Statement:* Development of Reports and the user interface must follow a collaborative, iterative, prototype-oriented methodology.

*Why discarded:* This specifies a project development process rather than behavior or a quality constraint of the deployed software.

#### BL-010 - Unavailable Configuration Migration

**Reason:** conflict &nbsp;·&nbsp; **Sources:** D14 &nbsp;·&nbsp; **Conflicts with:** FR-177 (Migrate Environment Configuration)

*Statement:* Configuration migration between development, testing, and production environments is not available.

*Why discarded:* This contradicts the later technical-subcommittee requirement to provide configuration migration, including export and import of Templates, permissions, and saved Queries. The later requirement is retained as "Migrate Environment Configuration".

#### BL-011 - Unavailable Real-Time Reporting

**Reason:** conflict &nbsp;·&nbsp; **Sources:** D14 &nbsp;·&nbsp; **Conflicts with:** NFR-019 (Real-Time Reporting Capability)

*Statement:* Real-time reporting is not available and all Reports run only on current data.

*Why discarded:* This conflicts with the stakeholder survey request for real-time or near-real-time reporting for operational monitoring. The retained requirement is "Real-Time Reporting Capability".

#### BL-012 - Limit SRS To Management Activities

**Reason:** out of scope &nbsp;·&nbsp; **Sources:** D17

*Statement:* The requirements specification should include only requirements directly or indirectly related to management activities.

*Why discarded:* This is a documentation-scoping decision for the requirements process, not a behavior, quality, or implementation constraint of the software.

#### BL-013 - Immediate Badge Login

**Reason:** conflict &nbsp;·&nbsp; **Sources:** D13 &nbsp;·&nbsp; **Conflicts with:** FR-001 (Staff Badge Authentication)

*Statement:* The system shall log a staff member in immediately after a successful badge swipe without requiring another credential.

*Why discarded:* This candidate conflicts with the kept authentication policy that a badge identifies the staff account but does not bypass individual authentication or a required second credential.

## 9. Open issues

Issues still reported when the review loop ended:

- **conflict** (major) (CON-019, CON-023, NFR-016, NFR-024, FR-174) [reviewer]: CON-019 requires reporting against the primary normalized database and disallows a synchronized copy, while CON-023 permits a separate reporting database or read-only replica, and FR-174 calls for a reporting warehouse or equivalent historical store. NFR-016 and NFR-024 also require reporting isolation and background processing, which may depend on the separated architecture. These requirements do not establish which architecture is permitted.
- **duplicate** (major) (FR-016, FR-149, D14-C43, D10-C167) [reviewer]: FR-016 requires a Patron count Canned Report grouped by home Branch, and FR-149 separately requires counts of Patrons grouped by home Branch. Both specify the same report capability; the canned-report aspect does not make the underlying count a distinct need.
- **missing_requirement** (major) (FR-189, D14-C09) [reviewer]: Candidate D14-C09 calls for access to full database fields. FR-189 says to expose relevant available fields and gives Item examples, but it does not clearly require the full reportable schema to be available. The qualifier “relevant” leaves room to omit fields that the candidate explicitly requested.
- **missing_requirement** (major) (FR-199, D04-C03) [reviewer]: D04-C03 includes sharing saved Queries, but FR-199 only requires saving and reusing definitions. FR-226 covers shared folders for Reports and Templates, not explicitly sharing Query definitions, so the candidate's sharing need is not clearly covered.
- **missing_requirement** (major) (FR-159, D10-C175, D14-C67) [reviewer]: The candidates request a list of Patrons with an inactive status, while FR-159 defines the result solely by absence of qualifying activity during an Inactivity period. A Patron's recorded inactive status may not be equivalent to that activity calculation, so reporting the status-based population is not assured.
- **inconsistent_terminology** (minor) (NFR-021, D06-C10) [reviewer]: The NFR-021 title uses “Audit Trail,” although the glossary specifies “Audit Log” as the standard term and says it replaces “audit trail.” The description itself uses “Audit Log,” making the terminology inconsistent within the requirement.
- **inconsistent_terminology** (minor) (FR-053, D03-C13, D09-C05) [reviewer]: FR-053 uses “Home Library,” while the glossary standardizes this concept as “Branch.” The same requirement uses “Branch” elsewhere, which makes the grouping terminology inconsistent.
- **weak_description** (minor) (NFR-020, D20-C24) [reviewer]: NFR-020 requires Reports to meet “acceptable response times” but provides no response-time thresholds. It says targets will be defined, leaving the performance requirement untestable until those targets are supplied.

## Review summary

The requirements contain a significant architecture conflict between direct reporting on the primary database and the use of replicas or a reporting warehouse. Several merged needs also remain uncovered or are duplicated, particularly Query sharing, full-field access, inactive-status reporting, and Patron counts by Branch. Resolve the major issues before approval.
