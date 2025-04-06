using MediatR;
using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class CreateCustomerCommand : BaseCommand, IRequest<Guid>
{
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? NationalCode { get; set; }
    public string? EconomicCode { get; set; }
    public string? Address { get; set; }
    public string? Phone { get; set; }
    public string? Email { get; set; }
    public bool IsActive { get; set; } = true;
} 