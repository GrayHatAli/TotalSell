namespace TotalSell.Domain.Entities;

public class Tag : BaseEntity
{
    public string Name { get; private set; }
    public string Code { get; private set; }
    public string Description { get; private set; }
    public bool IsActive { get; private set; }

    private Tag() { }

    public Tag(
        string name,
        string code,
        string description = null)
    {
        Name = name;
        Code = code;
        Description = description;
        IsActive = true;
    }

    public void Update(
        string name,
        string code,
        string description = null)
    {
        Name = name;
        Code = code;
        Description = description;
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