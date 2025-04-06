using Microsoft.AspNetCore.Mvc;
using MediatR;
using TotalSell.Application.Commands;
using TotalSell.Application.Queries;
using TotalSell.Application.DTOs;

namespace TotalSell.API.Controllers;

public class InvoicesController : BaseController
{
    public InvoicesController(IMediator mediator) : base(mediator)
    {
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<InvoiceDto>>> GetInvoices()
    {
        var query = new SearchInvoicesQuery();
        var result = await _mediator.Send(query);
        return Ok(result);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<InvoiceDto>> GetInvoice(Guid id)
    {
        var query = new GetInvoiceQuery { InvoiceId = id };
        var result = await _mediator.Send(query);
        if (result == null)
            return NotFound();
        return Ok(result);
    }

    [HttpPost]
    public async Task<ActionResult<Guid>> CreateInvoice(CreateInvoiceCommand command)
    {
        var result = await _mediator.Send(command);
        return CreatedAtAction(nameof(GetInvoice), new { id = result }, result);
    }

    [HttpPut("{id}")]
    public async Task<ActionResult> UpdateInvoice(Guid id, UpdateInvoiceCommand command)
    {
        if (id != command.Id)
            return BadRequest();
        
        await _mediator.Send(command);
        return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<ActionResult> DeleteInvoice(Guid id)
    {
        var command = new DeleteInvoiceCommand { Id = id };
        await _mediator.Send(command);
        return NoContent();
    }
} 