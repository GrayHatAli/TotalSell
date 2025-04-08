using MediatR;
using Microsoft.AspNetCore.Mvc;
using TotalSell.Application.Commands;
using TotalSell.Application.Queries;

namespace TotalSell.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class InvoicesController : ControllerBase
{
    private readonly IMediator _mediator;

    public InvoicesController(IMediator mediator)
    {
        _mediator = mediator;
    }

    [HttpGet]
    public async Task<IActionResult> GetInvoices([FromQuery] SearchInvoicesQuery query, CancellationToken cancellationToken)
    {
        var result = await _mediator.Send(query, cancellationToken);
        return Ok(result);
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetInvoice([FromRoute] Guid id, CancellationToken cancellationToken)
    {
        var query = new GetInvoiceQuery { Id = id };
        var result = await _mediator.Send(query, cancellationToken);
        return Ok(result);
    }

    [HttpPost]
    public async Task<IActionResult> CreateInvoice([FromBody] CreateInvoiceCommand command, CancellationToken cancellationToken)
    {
        var result = await _mediator.Send(command, cancellationToken);
        return CreatedAtAction(nameof(GetInvoice), new { id = result }, result);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateInvoice([FromRoute] Guid id, [FromBody] UpdateInvoiceCommand command, CancellationToken cancellationToken)
    {
        if (id != command.Id)
        {
            return BadRequest("ID mismatch");
        }

        var result = await _mediator.Send(command, cancellationToken);
        return Ok(result);
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteInvoice([FromRoute] Guid id, CancellationToken cancellationToken)
    {
        var command = new DeleteInvoiceCommand { Id = id };
        var result = await _mediator.Send(command, cancellationToken);
        return Ok(result);
    }
} 