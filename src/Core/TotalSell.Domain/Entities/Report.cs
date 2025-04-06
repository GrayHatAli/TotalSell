using System;
using TotalSell.Domain.Common;

namespace TotalSell.Domain.Entities;

public class Report : BaseEntity
{
    public string Name { get; private set; } = string.Empty;
    public string Description { get; private set; } = string.Empty;
    public string Category { get; private set; } = string.Empty;
    public string Type { get; private set; } = string.Empty;
    public string Query { get; private set; } = string.Empty;
    public string Parameters { get; private set; } = string.Empty;
    public string Format { get; private set; } = string.Empty;
    public string Status { get; private set; } = string.Empty;
    public bool IsActive { get; private set; }

    private Report() { }

    public Report(
        string name,
        string category,
        string type,
        string query,
        string parameters,
        string format,
        string? description = null)
    {
        Name = name;
        Description = description ?? string.Empty;
        Category = category;
        Type = type;
        Query = query;
        Parameters = parameters;
        Format = format;
        Status = "Active";
        IsActive = true;
    }

    public void Update(
        string name,
        string category,
        string type,
        string query,
        string parameters,
        string format,
        string? description = null)
    {
        Name = name;
        Description = description ?? string.Empty;
        Category = category;
        Type = type;
        Query = query;
        Parameters = parameters;
        Format = format;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Deactivate()
    {
        IsActive = false;
        Status = "Inactive";
        UpdatedAt = DateTime.UtcNow;
    }

    public void Activate()
    {
        IsActive = true;
        Status = "Active";
        UpdatedAt = DateTime.UtcNow;
    }
} 