### **Orchestrator Routing Rules (CORE LOGIC)**

**Rule 1: Emergency always wins**

```
IF intent_label == "emergency"
→ Trigger Human_Escalation_Prompt
→ End agent loop

```

**Rule 2: Emotional distress → support first**

```
IF intent_label IN ["feel_lonely", "feel_sad", "feel_anxious"]
→ Route to Psychological_Support_Prompt
→ Set needs_monitoring = true

```

**Rule 3: After support → monitor**

```
IF needs_monitoring == true
→ Route to Monitoring_Update_Prompt
→ Capture mood_score

```

**Rule 4: Low mood persistence**

```
IF mood_score <= 4
→ Increment low_mood_counter
ELSE
→ Reset low_mood_counter

```

**Rule 5: Escalation threshold**

```
IF low_mood_counter >= 3
→ Trigger Human_Escalation_Prompt
→ End agent loop

```

**Rule 6: Otherwise → wellness**

```
IF escalation_flag == false
→ Route to Wellness_Action_Prompt

```

**Rule 7: Safe completion**

```
End conversation gracefully
```

