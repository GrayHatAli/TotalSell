namespace TotalSell.Application.Commands;

public abstract class BaseCommand
{
    public Guid Id { get; set; }
    public DateTime Timestamp { get; set; }
    public string? UserId { get; set; }
} 