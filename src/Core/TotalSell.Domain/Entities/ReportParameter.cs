namespace TotalSell.Domain.Entities;

public class ReportParameter : BaseEntity
{
    public Guid ReportId { get; private set; }
    public Report? Report { get; private set; }
    public string Name { get; private set; } = string.Empty;
    public string Label { get; private set; } = string.Empty;
    public string DataType { get; private set; } = string.Empty;
    public string DefaultValue { get; private set; } = string.Empty;
    public bool IsRequired { get; private set; }
    public string ValidationRule { get; private set; } = string.Empty;
    public string Options { get; private set; } = string.Empty;
    public int Order { get; private set; }
    public bool IsActive { get; private set; }

    private ReportParameter() { }

    public ReportParameter(
        Guid reportId,
        string name,
        string label,
        string dataType,
        string? defaultValue = null,
        bool isRequired = false,
        string? validationRule = null,
        string? options = null,
        int order = 0)
    {
        ReportId = reportId;
        Name = name;
        Label = label;
        DataType = dataType;
        DefaultValue = defaultValue ?? string.Empty;
        IsRequired = isRequired;
        ValidationRule = validationRule ?? string.Empty;
        Options = options ?? string.Empty;
        Order = order;
        IsActive = true;
    }

    public void UpdateDetails(
        string label,
        string dataType,
        string defaultValue,
        bool isRequired,
        string validationRule,
        string options,
        int order)
    {
        Label = label;
        DataType = dataType;
        DefaultValue = defaultValue;
        IsRequired = isRequired;
        ValidationRule = validationRule;
        Options = options;
        Order = order;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Deactivate()
    {
        IsActive = false;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Activate()
    {
        IsActive = true;
        UpdatedAt = DateTime.UtcNow;
    }
} 