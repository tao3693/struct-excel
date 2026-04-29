# Excel Data Query Operation Manual

This manual provides a step-by-step guide on how to perform cross-table data queries in Excel using the 5 provided datasets (Enrollments, Students, Supervisors, Sessions, and Courses) without using complex formulas.

---

## 1. Understanding Data Relationships

To perform queries correctly, you must understand how the 5 tables connect to each other:

1. **The Hub**: Everything starts from the **`enrollments`** table.
2. **Students**: `enrollments` links to **`students`** via the `student_id` field.
3. **Supervisors**: `students` links to **`supervisors`** via the `supervisor_id` field.
4. **Sessions**: `enrollments` links to **`sessions`** via the `session_id` field.
5. **Courses**: `sessions` links to **`courses`** via the `course_id` field.

---

## 2. Setup: Importing and Connecting Data

### Step 1: Import Data correctly

1. Open a **new, blank** Excel workbook.
2. Go to the **Data** tab ➡️ **Get Data** ➡️ **From File** ➡️ **From Text/CSV**.
3. Select your first file (e.g., `enrollments.csv`) and click **Import**.
4. **CRITICAL**: In the preview window, do **NOT** click "Load". Click the arrow next to "Load" and select **Load To...**.
5. Select **Only Create Connection** AND check the box **Add this data to the Data Model**. Click **OK**.
6. Repeat these steps for the remaining 4 files.

### Step 2: Create Relationships (The "Red Strings")

1. Go to the **Data** tab ➡️ click **Data Model** (Management) icon (usually an icon with a green checkmark).
2. In the Power Pivot window that opens, click **Diagram View** (top right).
3. You will see 5 boxes representing your tables. Use your mouse to **drag and drop** to create the following 4 connections:
   * Drag `student_id` from `enrollments` to `student_id` in `students`.
   * Drag `session_id` from `enrollments` to `session_id` in `sessions`.
   * Drag `course_id` from `sessions` to `course_id` in `courses`.
   * Drag `supervisor_id` from `students` to `supervisor_id` in `supervisors`.
4. Once the 4 lines are visible, close the Power Pivot window.

---

## 3. Querying Data using PivotTables

1. In your Excel sheet, go to **Insert** ➡️ **PivotTable** ➡️ **From Data Model**. Click **OK**.
2. The **PivotTable Fields** panel will appear on the right, showing all 5 tables.

> 🌟 **THE GOLDEN RULE** 🌟
> Whenever you perform a query, you **MUST** drag an ID field (like `student_id` or `enrollment_id`) into the **Values** area at the bottom right.
>
> *Why?* Excel only calculates the relationships between tables when it is forced to "count" or "calculate" something. Without a value, filters from one table might not affect the display of another table.

---

## 4. Practical Query Scenarios

### Scenario A: Which students are under a specific supervisor (e.g., SMS)?

1. Expand the `supervisors` table and drag **`full_name`** to the **Filters** area.
2. Expand the `students` table and drag **`full_name`** and **`company`** to the **Rows** area.
3. Drag **`student_id`** from the `students` table to the **Values** area.
4. Now, use the filter at the top of your sheet to select "SMS". The list will instantly update to show only his students.

### Scenario B: How many enrollments are there for each course?

1. Expand the `courses` table and drag **`course_name`** to the **Rows** area.
2. Expand the `enrollments` table and drag **`enrollment_id`** to the **Values** area.
3. Excel will display the total enrollment count for every course.

### Scenario C: List of pending payments by company

1. Expand `enrollments` and drag **`payment_status`** to the **Filters** area. Set the filter to **`PENDING`**.
2. Expand `students` and drag **`company`** to the **Rows** area.
3. Drag **`student_id`** from `students` to the **Values** area.
4. You now have a neat list showing which companies have pending payments and how many.

---

## 5. Troubleshooting

If a filter is not working:

1. Check if you have a field in the **Values** area.
2. Go back to **Data > Data Model > Diagram View** and ensure the lines are connecting the correct matching ID fields.
